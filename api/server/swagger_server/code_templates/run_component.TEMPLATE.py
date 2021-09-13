# Copyright 2021 IBM Corporation
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
def kfp_component_pipeline(${pipeline_method_args}):

    from kfp import components

    template_url = '${component_template_url}'

    comp = components.load_component_from_url(template_url)

    op = comp(${parameter_names})


############################################################
#              Compile the pipeline
############################################################

pipeline_function = kfp_component_pipeline
pipeline_filename = path.join(gettempdir(),
                              pipeline_function.__name__ + '.pipeline.tar.gz')

TektonCompiler().compile(pipeline_function, pipeline_filename)

############################################################
#              Run the pipeline
############################################################

# TODO: specify pipeline argument values
arguments = ${parameter_dict}

client = TektonClient(${pipeline_server})

# Get or create an experiment and submit a pipeline run
experiment = client.create_experiment('COMPONENT_RUNS')

# Submit the experiment to run in a pipeline
run_name = '${run_name}'
run_result = client.run_pipeline(experiment.id, run_name, pipeline_filename, arguments)
