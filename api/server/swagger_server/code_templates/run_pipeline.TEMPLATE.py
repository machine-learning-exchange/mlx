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
    name='${name}',
    description='${description}'
)
def custom_pipeline(${pipeline_method_args}):  # noqa: E999

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

client = TektonClient(${pipeline_server})  # noqa: E999

# Get or create an experiment and submit a pipeline run
experiment = client.create_experiment('PIPELINE_RUNS')

# Submit the experiment to run in a pipeline
run_name = '${run_name}'
run_result = client.run_pipeline(experiment.id, run_name, pipeline_file, arguments)
