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
from kfp import components
import json

secret_name = 'wml-creds'
generated_secret = 'test-creds'

train_op = components.load_component_from_url('https://raw.githubusercontent.com/kubeflow/pipelines/master/components/ibm-components/watson/train/component.yaml')


@dsl.pipeline(
  name='Model Training pipeline',
  description='A pipeline for ML/DL model training using Watson Machine Learning.'
)
def modelPipeline(
    model_id='max-image-completer'
):

    """A pipeline for ML/DL model deployment."""

    # define workflow
    model_config = dsl.ContainerOp(
     name='model_config',
     image='tomcli/model-config:latest',
     command=['python'],
     arguments=['-u', 'model-config.py',
                '--secret_name', generated_secret,
                '--model_id', model_id],
     file_outputs={'train_code': '/tmp/train_code',
                   'execution_command': '/tmp/execution_command',
                   'framework': '/tmp/framework',
                   'framework_version': '/tmp/framework_version',
                   'runtime': '/tmp/runtime',
                   'runtime_version': '/tmp/runtime_version',
                   'run_definition': '/tmp/run_definition',
                   'run_name': '/tmp/run_name'
                   }).apply(params.use_ai_pipeline_params(secret_name))

    wml_train = train_op(
                   train_code=model_config.outputs['train_code'],
                   execution_command=model_config.outputs['execution_command'],
                   framework=model_config.outputs['framework'],
                   framework_version=model_config.outputs['framework_version'],
                   runtime=model_config.outputs['runtime'],
                   runtime_version=model_config.outputs['runtime_version'],
                   run_definition=model_config.outputs['run_definition'],
                   run_name=model_config.outputs['run_name']
                   ).apply(params.use_ai_pipeline_params(generated_secret))


if __name__ == '__main__':
    import kfp.compiler as compiler
    compiler.Compiler().compile(modelPipeline, __file__ + '.tar.gz')
