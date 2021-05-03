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

@dsl.pipeline(
  name='cp4d-scoring-monitoring',
  description='A pipeline for Deploying model scoring and monitoring service'
)
def icpd_scoring_monitoring(
    kfservice_url='istio-ingressgateway.istio-system:80',
    kafka_brokers='my-cluster-kafka-bootstrap.kubeflow:9092',
    kafka_apikey='',
    telemetry_topic='reeferTelemetries',
    container_topic='containers',
    model_serving_metadata='{"apiVersion":"serving.kubeflow.org/v1alpha1","kind":"KFService","metadata":{"annotations":{"autoscaling.knative.dev/target":"10"},"creationTimestamp":"2019-10-04T18:44:59Z","generation":1,"name":"maintenance-model-pg","namespace":"model-deploy","resourceVersion":"153452239","selfLink":"/apis/serving.kubeflow.org/v1alpha1/namespaces/model-deploy/kfservices/maintenance-model-pg","uid":"1130647c-e6d7-11e9-8107-06078924dd3e"},"spec":{"canary":{"custom":{"container":{"env":[{"name":"MODEL_PATH","value":"model_logistic_regression_pg.pkl"}],"image":"tomcli/webapp:v0.0.4","name":"maintenance-model-pg","ports":[{"containerPort":8080}],"resources":{"requests":{"cpu":"1","memory":"2Gi"}}}}},"canaryTrafficPercent":10,"default":{"custom":{"container":{"env":[{"name":"MODEL_PATH","value":"model_logistic_regression_pg.pkl"}],"image":"tomcli/webapp:v0.0.4","name":"maintenance-model-pg","ports":[{"containerPort":8080}],"resources":{"requests":{"cpu":"1","memory":"2Gi"}}}}}},"status":{"canary":{"name":"maintenance-model-pg-canary-qhmvr","traffic":10},"conditions":[{"lastTransitionTime":"2019-10-22T21:13:30Z","message":"Revision \"maintenance-model-pg-canary-qhmvr\" failed with message: 0/1 nodes are available: 1 Insufficient cpu..","reason":"RevisionFailed","severity":"Info","status":"False","type":"CanaryPredictorReady"},{"lastTransitionTime":"2019-10-22T21:13:30Z","message":"Revision \"maintenance-model-pg-default-8pcqz\" failed with message: 0/1 nodes are available: 1 Insufficient cpu..","reason":"RevisionFailed","status":"False","type":"DefaultPredictorReady"},{"lastTransitionTime":"2019-10-22T21:13:30Z","message":"Revision \"maintenance-model-pg-default-8pcqz\" failed with message: 0/1 nodes are available: 1 Insufficient cpu..","reason":"RevisionFailed","status":"False","type":"Ready"},{"lastTransitionTime":"2019-10-29T16:58:46Z","status":"True","type":"RoutesReady"}],"default":{"name":"maintenance-model-pg-default-8pcqz","traffic":90},"url":"http://maintenance-model-pg.model-deploy.example.com"}}',
    secret_name = 'icp4d-demo',
    credentials_id = ''
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
    scoring = kubedeploy_ops(component_name='scoring',
                             deployment_image='aipipeline/predictivescoring:v0.0.3',
                             deployment_name='scoring',
                             container_port='8080',
                             kafka_brokers=kafka_brokers,
                             kafka_apikey=kafka_apikey,
                             telemetry_topic=telemetry_topic,
                             container_topic=container_topic,
                             kfservice_url=kfservice_url,
                             model_serving_metadata=model_serving_metadata).apply(params.use_ai_pipeline_params('{{workflow.parameters.secret-name}}'))
    monitoring = kubedeploy_ops(component_name='monitoring',
                                deployment_image='ffdlops/consumer:v0.0.1',
                                deployment_name='customer',
                                container_port='8080',
                                kafka_brokers=kafka_brokers,
                                kafka_apikey=kafka_apikey).after(scoring).apply(params.use_ai_pipeline_params('{{workflow.parameters.secret-name}}'))

    post_template_url = 'https://raw.githubusercontent.com/Tomcli/kfp-components/master/postprocessing.yaml'
    post_model_ops = components.load_component_from_url(post_template_url)
    post_model = post_model_ops(notification_type='other',
                                pipeline_name='{{pod.name}}').apply(params.use_ai_pipeline_params('{{workflow.parameters.credentials-id}}')).after(monitoring).set_image_pull_policy('Always')


if __name__ == '__main__':
    import kfp.compiler as compiler
    compiler.Compiler().compile(icpd_scoring_monitoring, __file__ + '.tar.gz')
