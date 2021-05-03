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


kfserving_ops = components.load_component_from_file('kfserving.yaml')
notebook_ops = components.load_component_from_file('notebook.yaml')
setup_ops = components.load_component_from_file('setup.yaml')
post_model_ops = components.load_component_from_file('postprocessing.yaml')

@dsl.pipeline(
  name='icp4d-demo',
  description='A pipeline for training using Jupyter notebook and Serve models with KFServing'
)
def icpdPipeline(
    notebook_url='https://raw.githubusercontent.com/animeshsingh/notebooks/master/sklearn.ipynb',
    notebook_params='',
    api_token='',
    endpoint_url='minio-service:9000',
    bucket_name='mlpipeline',
    object_name='notebooks/sklearn-model/runs/train/sklearn-pg_out.ipynb',
    access_key='minio',
    secret_access_key='minio123',
    kfservice_url='istio-ingressgateway.istio-system:80',
    action='update',
    model_name='maintenance-model-pg',
    model_deploy_namespace='model-deploy',
    default_custom_model_spec='{"name": "maintenance-model-pg", "image": "tomcli/webapp:v0.0.4", "port": "8080", "env": [{"name": "MODEL_PATH", "value": "model_logistic_regression_pg.pkl"}]}',
    canary_custom_model_spec='{"name": "maintenance-model-pg", "image": "tomcli/webapp:v0.0.4", "port": "8080", "env": [{"name": "MODEL_PATH", "value": "model_logistic_regression_pg.pkl"}]}',
    canary_model_traffic_percentage='10',
    autoscaling_target='10',
    kafka_brokers='my-cluster-kafka-bootstrap.kubeflow:9092',
    kafka_apikey='',
    telemetry_topic='reeferTelemetries',
    container_topic='containers',
    remote_kfserving_deployer_api='',
    remote_istio_ingress_endpoint='',
    credentials_id = '',
    secret_name = 'icp4d-demo'
):

    def kubedeploy_ops(component_name, deployment_image, deployment_name, container_port, cleanup='False',
                       namespace='kubeflow', kafka_brokers=kafka_brokers, kafka_apikey=kafka_apikey,
                       telemetry_topic=telemetry_topic, container_topic=container_topic,
                       kfservice_url=kfservice_url, model_serving_metadata=''):
        return dsl.ContainerOp(
            name=component_name,
            image='docker.io/aipipeline/kafka-app-deployment:v0.7',
            command=['python'],
            arguments=[
                '-u', 'kube_deployment.py',
                '--model_serving_image', deployment_image,
                '--deployment_name', deployment_name,
                "--container_port", container_port,
                "--cleanup", cleanup,
                "--namespace", namespace,
                "--env_kafka_brokers", kafka_brokers,
                "--env_kafka_apikey", kafka_apikey,
                "--env_telemetry_topic", telemetry_topic,
                "--env_container_topic", container_topic,
                "--env_kfservice_url", kfservice_url,
                "--env_model_serving_metadata", model_serving_metadata
            ],
            file_outputs={'logs': '/tmp/log.txt'}
        )

    setup = setup_ops(secret_name=('{{workflow.parameters.credentials-id}}-cred')).apply(params.use_ai_pipeline_params('{{workflow.parameters.credentials-id}}'))

    trainer_notebook = notebook_ops(notebook_url=notebook_url,
                                    notebook_params=notebook_params,
                                    api_token=api_token,
                                    endpoint_url=endpoint_url,
                                    bucket_name=bucket_name,
                                    object_name=object_name,
                                    access_key=access_key,
                                    secret_access_key=secret_access_key).add_env_variable(
                                        k8s_client.V1EnvVar(
                                            name='POSTGRES_URL',
                                            value_from=k8s_client.V1EnvVarSource(
                                                secret_key_ref=k8s_client.V1SecretKeySelector(
                                                    name='{{workflow.parameters.credentials-id}}-cred',
                                                    key='POSTGRES_URL'
                                                )
                                            )
                                        )
                                    ).after(setup)
    postprocessing_1 = post_model_ops().apply(params.use_ai_pipeline_params('{{workflow.parameters.credentials-id}}')).after(trainer_notebook).set_image_pull_policy('Always')
    serving = kfserving_ops(action=action,
                            model_name=model_name,
                            namespace=model_deploy_namespace,
                            framework='custom',
                            default_custom_model_spec=default_custom_model_spec,
                            canary_custom_model_spec=canary_custom_model_spec,
                            canary_model_traffic_percentage=canary_model_traffic_percentage,
                            autoscaling_target=autoscaling_target,
                            kfserving_deployer_api=remote_kfserving_deployer_api).after(trainer_notebook)
    postprocessing_2 = post_model_ops(notification_type='serving', serving_output=serving.outputs['endpoint_uri']).apply(params.use_ai_pipeline_params('{{workflow.parameters.credentials-id}}')).set_image_pull_policy('Always').apply(params.use_ai_pipeline_params('{{workflow.parameters.secret-name}}', secret_volume_mount_path='/app/ip'))
    scoring = kubedeploy_ops(component_name='scoring',
                             deployment_image='aipipeline/predictivescoring:v0.0.3',
                             deployment_name='scoring',
                             container_port='8080',
                             kafka_brokers=kafka_brokers,
                             kafka_apikey=kafka_apikey,
                             telemetry_topic=telemetry_topic,
                             container_topic=container_topic,
                             kfservice_url=kfservice_url,
                             model_serving_metadata=serving.outputs['endpoint_uri']).apply(params.use_ai_pipeline_params('{{workflow.parameters.secret-name}}'))
    monitoring = kubedeploy_ops(component_name='monitoring',
                                deployment_image='ffdlops/consumer:v0.0.1',
                                deployment_name='customer',
                                container_port='8080',
                                kafka_brokers=kafka_brokers,
                                kafka_apikey=kafka_apikey).after(scoring).apply(params.use_ai_pipeline_params('{{workflow.parameters.secret-name}}'))
    postprocessing_3 = post_model_ops(notification_type='other',
                                      pipeline_name='{{pod.name}}').apply(params.use_ai_pipeline_params('{{workflow.parameters.credentials-id}}')).after(monitoring).set_image_pull_policy('Always')

if __name__ == '__main__':
    import kfp.compiler as compiler
    compiler.Compiler().compile(icpdPipeline, __file__ + '.tar.gz')
