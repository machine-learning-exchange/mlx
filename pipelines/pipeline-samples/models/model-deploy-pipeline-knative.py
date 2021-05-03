# Copyright 2021 IBM Corporation
# 
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
import kfp.dsl as dsl
import ai_pipeline_params as params
import json

secret_name = 'e2e-creds'

@dsl.pipeline(
  name='Model Deployment pipeline',
  description='A pipeline for ML/DL model deployment using Knative.'
)
def modelPipeline(
    model_id='max-image-caption-generator'
):

    """A pipeline for ML/DL model deployment."""

    # define workflow
    model_config = dsl.ContainerOp(
     name='model_config',
     image='tomcli/model-config',
     command=['python'],
     arguments=['-u', 'model-config.py',
                '--secret_name', secret_name,
                '--model_id', model_id],
     file_outputs={'model_serving_image': '/tmp/model_serving_image',
                   'primary_model_revision': '/tmp/primary_model_revision',
                   'deployment_name': '/tmp/deployment_name'})

    model_deployment = dsl.ContainerOp(
     name='knative_model_deployment',
     image='aipipeline/knative-model-deploy',
     command=['python'],
     arguments=['-u', 'knative_deployment.py',
                '--model_serving_image', model_config.outputs['model_serving_image'],
                '--primary_model_revision', model_config.outputs['primary_model_revision'],
                '--deployment_name', model_config.outputs['deployment_name']],
     file_outputs={'output': '/tmp/log.txt'}).apply(params.use_ai_pipeline_params(secret_name))


if __name__ == '__main__':
    import kfp.compiler as compiler
    compiler.Compiler().compile(modelPipeline, __file__ + '.tar.gz')
