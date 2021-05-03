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
def custom_pipeline(${pipeline_method_args}):

    ${pipeline_function_body}


############################################################
#              Compile the pipeline
############################################################

pipeline_func = custom_pipeline
pipeline_file = path.join(gettempdir(), pipeline_func.__name__ + '.pipeline.tar.gz')

TektonCompiler().compile(pipeline_func, pipeline_file)

############################################################
#              Run the pipeline
############################################################

# TODO: specify pipeline argument values
arguments = ${parameter_dict}

client = TektonClient(${pipeline_server})

# Get or create an experiment and submit a pipeline run
experiment = client.create_experiment('PIPELINE_RUNS')

# Submit the experiment to run in a pipeline
run_name = '${run_name}'
run_result = client.run_pipeline(experiment.id, run_name, pipeline_file, arguments)
