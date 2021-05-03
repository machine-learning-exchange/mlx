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
                             namespace='anonymous',
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

client = TektonClient(${pipeline_server})

# Get or create an experiment and submit a pipeline run
experiment = client.create_experiment('MODEL_RUNS')

# Submit the experiment to run in a pipeline
run_name = '${run_name}'
run_result = client.run_pipeline(experiment.id, run_name, pipeline_filename)
