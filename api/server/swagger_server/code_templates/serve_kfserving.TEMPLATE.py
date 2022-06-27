# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0

from kfp import dsl
from kfp_tekton.compiler import TektonCompiler
from kfp_tekton import TektonClient
from os import path
from tempfile import gettempdir


############################################################
#              Define the pipeline method
############################################################

@dsl.pipeline(
    name='KFServing pipeline',
    description='A pipeline for serving models with KFServing'
)
def model_pipeline(model_id='${model_identifier}'):
    """A pipeline to serve models with KFServing."""

    import ai_pipeline_params as params
    from kfp import components
    from kfp import dsl

    secret_name = 'e2e-creds'

    template_url = 'https://raw.githubusercontent.com/Tomcli/pipelines/35112b844ff3c9cc92a186fcb9abac646271ef02/components/kubeflow/kfserving/component.yaml'

    kfserving_op = components.load_component_from_url(template_url)

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
            'default-custom-model-spec': '/tmp/default_custom_model_spec',
            'deployment-name': '/tmp/deployment_name',
            'container-port': '/tmp/container_port'
        }
    )

    kfserving = kfserving_op(action='apply',
                             model_name=model_id,
                             namespace='mlx',  # TODO: use a variable 'namespace' for multi-user deployment
                             framework='custom',
                             default_custom_model_spec=model_config.outputs['default-custom-model-spec']).set_image_pull_policy('Always')

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

client = TektonClient(${pipeline_server})  # noqa: E999

# Get or create an experiment and submit a pipeline run
experiment = client.create_experiment('MODEL_RUNS')

# Submit the experiment to run in a pipeline
run_name = '${run_name}'
run_result = client.run_pipeline(experiment.id, run_name, pipeline_filename)
