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
    name='${name}',
    description='${description}'
)
def dataset_pipeline(${pipeline_method_args}):

    from kfp.components import load_component_from_url

    dax_dataset_metadata_url = '${dataset_template_url}'
    dax_to_dlf_component_url = '${dax_to_dlf_component_url}'
    dlf_to_pvc_component_url = '${dlf_to_pvc_component_url}'

    dax_to_dlf_op = load_component_from_url(dax_to_dlf_component_url)
    dlf_to_pvc_op = load_component_from_url(dlf_to_pvc_component_url)

    create_dlf_yaml = dax_to_dlf_op(dax_yaml=dax_dataset_metadata_url)\
        .set_image_pull_policy('Always')\
        .set_display_name("generate dataset metadata")

    mount_pvc = dlf_to_pvc_op(action='create',
                              namespace='${namespace}',
                              dataset_yaml=create_dlf_yaml.outputs['dlf_yaml'])\
        .set_image_pull_policy('Always')\
        .set_display_name("create persistent volume")


############################################################
#              Compile the pipeline
############################################################

pipeline_function = dataset_pipeline
pipeline_filename = path.join(gettempdir(), pipeline_function.__name__ + '.pipeline.tar.gz')

TektonCompiler().compile(pipeline_function, pipeline_filename)

############################################################
#              Run the pipeline
############################################################

# TODO: specify pipeline argument values
arguments = ${parameter_dict}

client = TektonClient(${pipeline_server})

# Get or create an experiment and submit a pipeline run
experiment = client.create_experiment('DATASET_RUNS')

# Submit the experiment to run in a pipeline
run_name = '${run_name}'
run_result = client.run_pipeline(experiment.id, run_name, pipeline_filename, arguments)
