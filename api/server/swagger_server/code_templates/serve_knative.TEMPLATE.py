# Copyright 2021 The MLX Contributors
# 
# SPDX-License-Identifier: Apache-2.0 

from kfp import dsl
from kfp_tekton.compiler import TektonCompiler
from kfp_tekton import TektonClient
from os import path
from tempfile import gettempdir


############################################################
#   Define the pipeline method
############################################################

@dsl.pipeline(
    name='Model Deployment pipeline',
    description='A pipeline for ML/DL model deployment using Knative.'
)
def model_pipeline(model_id='${model_identifier}'):
    """A pipeline for ML/DL model deployment."""

    from kfp import dsl
    from ai_pipeline_params import use_ai_pipeline_params

    secret_name = 'e2e-creds'

    model_config = dsl.ContainerOp(
        name='model_config',
        image='tomcli/model-config',
        command=['python'],
        arguments=[
            '-u', 'model-config.py',
            '--secret_name', secret_name,
            '--model_id', model_id
        ],
        file_outputs={
            'model_serving_image': '/tmp/model_serving_image',
            'primary_model_revision': '/tmp/primary_model_revision',
            'deployment_name': '/tmp/deployment_name'
        }
    )

    model_deployment = dsl.ContainerOp(
        name='knative_model_deployment',
        image='aipipeline/knative-model-deploy',
        command=['python'],
        arguments=[
            '-u', 'knative_deployment.py',
            '--model_serving_image', model_config.outputs['model_serving_image'],
            '--primary_model_revision', model_config.outputs['primary_model_revision'],
            '--deployment_name', model_config.outputs['deployment_name']
        ],
        file_outputs={
            'output': '/tmp/log.txt'
        }
    )

    model_deployment.apply(use_ai_pipeline_params(secret_name))


############################################################
#   Compile the pipeline
############################################################

pipeline_function = model_pipeline
pipeline_filename = path.join(gettempdir(),
                              pipeline_function.__name__ + '.tar.gz')

TektonCompiler().compile(pipeline_function, pipeline_filename)

############################################################
#   Run the pipeline
############################################################

client = TektonClient(${pipeline_server})  # noqa: E999

# Get or create an experiment and submit a pipeline run
experiment = client.create_experiment('MODEL_RUNS')

# Submit the experiment to run in a pipeline
run_name = '${run_name}'
run_result = client.run_pipeline(experiment.id, run_name, pipeline_filename)
