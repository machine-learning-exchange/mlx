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

from kfp import dsl
from kfp_tekton.compiler import TektonCompiler
from kfp_tekton import TektonClient
from os import path
from tempfile import gettempdir


############################################################
#              Define the pipeline method
############################################################

@dsl.pipeline(
    name='Model Training pipeline',
    description='A pipeline for ML/DL model training using Watson Machine Learning.'
)
def model_pipeline(model_id='${model_identifier}'):
    """A pipeline for ML/DL model deployment."""

    from kfp import components, dsl
    from ai_pipeline_params import use_ai_pipeline_params

    secret_name = 'wml-creds'
    generated_secret = 'test-creds'

    train_op = components.load_component_from_url(
        'https://raw.githubusercontent.com/kubeflow/pipelines/master/components/ibm-components/watson/train/component.yaml')

    model_config = dsl.ContainerOp(
        name='model_config',
        image='tomcli/model-config:latest',
        command=['python'],
        arguments=[
            '-u', 'model-config.py',
            '--secret_name', generated_secret,
            '--model_id', model_id
        ],
        file_outputs={
            'train_code': '/tmp/train_code',
            'execution_command': '/tmp/execution_command',
            'framework': '/tmp/framework',
            'framework_version': '/tmp/framework_version',
            'runtime': '/tmp/runtime',
            'runtime_version': '/tmp/runtime_version',
            'run_definition': '/tmp/run_definition',
            'run_name': '/tmp/run_name'
        }
    )

    model_config.apply(use_ai_pipeline_params(secret_name))

    model_training = train_op(
        train_code=model_config.outputs['train_code'],
        execution_command=model_config.outputs['execution_command'],
        framework=model_config.outputs['framework'],
        framework_version=model_config.outputs['framework_version'],
        runtime=model_config.outputs['runtime'],
        runtime_version=model_config.outputs['runtime_version'],
        run_definition=model_config.outputs['run_definition'],
        run_name=model_config.outputs['run_name']
    )

    model_training.apply(use_ai_pipeline_params(generated_secret))


############################################################
#              Compile the pipeline
############################################################

pipeline_function = model_pipeline
pipeline_filename = path.join(gettempdir(),
                              pipeline_function.__name__ + '.tar.gz')

TektonCompiler().compile(pipeline_function, pipeline_filename)

############################################################
#              Run the pipeline
############################################################

client = TektonClient(${pipeline_server})

# Get or create an experiment and submit a pipeline run
experiment = client.create_experiment('MODEL_RUNS')

# Submit the experiment to run in a pipeline
run_name = '${run_name}'
run_result = client.run_pipeline(experiment.id, run_name, pipeline_filename)
