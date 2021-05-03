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
    credentials_id = '',
):

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
    post_model = post_model_ops().apply(params.use_ai_pipeline_params('{{workflow.parameters.credentials-id}}')).after(trainer_notebook).set_image_pull_policy('Always')


if __name__ == '__main__':
    import kfp.compiler as compiler
    compiler.Compiler().compile(icpdPipeline, __file__ + '.tar.gz')
