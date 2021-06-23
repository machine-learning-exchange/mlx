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
    name='Model Deployment pipeline',
    description='A pipeline for ML/DL model deployment on Kubernetes.'
)
def model_pipeline(model_id='${model_identifier}'):
    """A pipeline for ML/DL model deployment."""

    from kfp import dsl
    from ai_pipeline_params import use_ai_pipeline_params

    secret_name = 'e2e-creds'

    model_config = dsl.ContainerOp(
        name='model_config',
        image='aipipeline/model-config',
        command=['python'],
        arguments=[
            '-u', 'model-config.py',
            '--secret_name', secret_name,
            '--model_id', model_id
        ],
        file_outputs={
            'model-serving-image': '/tmp/model_serving_image',
            'deployment-name': '/tmp/deployment_name'
        }
    )

    model_deployment = dsl.ContainerOp(
        name='k8s_model_deployment',
        image='aipipeline/deployment-k8s-remote',
        command=['python'],
        arguments=[
            '-u', 'kube_deployment.py',
            '--model_serving_image', model_config.outputs['model-serving-image'],
            '--deployment_name', model_config.outputs['deployment-name']
        ],
        file_outputs={
            'output': '/tmp/log.txt'
        }
    )

    model_deployment.apply(use_ai_pipeline_params(secret_name))


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
