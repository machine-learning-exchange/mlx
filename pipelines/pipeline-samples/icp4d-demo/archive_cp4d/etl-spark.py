# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from kfp import dsl
from kfp import compiler
from kfp import components
from kubernetes import client as k8s_client
import ai_pipeline_params as params
import json

setup_ops = components.load_component_from_file('setup.yaml')
etl_ops = components.load_component_from_file('etl.yaml')
push_ops = components.load_component_from_file('push.yaml')

@dsl.pipeline(
  name='etl-demo',
  description='A pipeline for Spark-based ETL from Kafka to PostgreSQL.'
)

def etlPipeline(
    spark_master='local[*]',
    kafka_bootstrap_servers='my-cluster-kafka-bootstrap.kubeflow:9092',
    kafka_topic='reefer',
    batch_temp_loc='batch.csv',
    table_name='reefer_telemetries',
    credentials_id = ''
):

    setup = setup_ops(secret_name=('{{workflow.parameters.credentials-id}}-cred')).apply(params.use_ai_pipeline_params('{{workflow.parameters.credentials-id}}'))

    push = push_ops(kafka_bootstrap_servers=kafka_bootstrap_servers,
                    kafka_topic=kafka_topic).after(setup)

    etl = etl_ops(spark_master=spark_master,
                  kafka_bootstrap_servers=kafka_bootstrap_servers,
                  kafka_topic=kafka_topic,
                  batch_temp_loc=batch_temp_loc,
                  table_name=table_name).add_env_variable(
                      k8s_client.V1EnvVar(
                          name='POSTGRES_URL',
                          value_from=k8s_client.V1EnvVarSource(
                              secret_key_ref=k8s_client.V1SecretKeySelector(
                                  name='{{workflow.parameters.credentials-id}}-cred',
                                  key='POSTGRES_URL'
                              )
                          )
                      )
                  ).set_image_pull_policy('Always').after(push)

    post_template_url = 'https://raw.githubusercontent.com/Tomcli/kfp-components/master/postprocessing.yaml'
    post_model_ops = components.load_component_from_url(post_template_url)
    post_model = post_model_ops(notification_type='etl',
                                pipeline_name='{{pod.name}}').apply(params.use_ai_pipeline_params('{{workflow.parameters.credentials-id}}')).after(etl).set_image_pull_policy('Always')

if __name__ == '__main__':
    import kfp.compiler as compiler
    compiler.Compiler().compile(etlPipeline, __file__ + '.tar.gz')
