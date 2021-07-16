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
    name='Run Jupyter Notebook ${name}',
    description='A pipeline to run a Jupyter notebook using the elyra-ai/kfp-notebook library.'
)
def notebook_pipeline():
    """A pipeline to run a Jupyter notebook with elyra-ai/kfp-notebook and Papermill."""

    from kfp_notebook.pipeline import NotebookOp

    notebook_op = NotebookOp(name="${name}",
                             pipeline_name="run-jupyter-notebook-${name}",
                             experiment_name="NOTEBOOK_RUNS",
                             notebook="${notebook}",
                             cos_endpoint="${cos_endpoint}",
                             cos_bucket="${cos_bucket}",
                             cos_directory="${cos_directory}",
                             cos_dependencies_archive="${cos_dependencies_archive}",
                             requirements_url="${requirements_url}",
                             image="${image}")

    from kubernetes.client.models import V1EnvVar

    notebook_op.container.add_env_variable(V1EnvVar(name='AWS_ACCESS_KEY_ID', value="${cos_username}"))
    notebook_op.container.add_env_variable(V1EnvVar(name='AWS_SECRET_ACCESS_KEY', value="${cos_password}"))

    from kfp import onprem

    notebook_op.container.add_env_variable(V1EnvVar(name='DATA_DIR', value="${mount_path}"))
    notebook_op.apply(onprem.mount_pvc(pvc_name='${dataset_pvc}',
                                       volume_name='${dataset_pvc}',
                                       volume_mount_path='${mount_path}'))


############################################################
#              Compile the pipeline
############################################################

pipeline_function = notebook_pipeline
pipeline_filename = path.join(gettempdir(),
                              pipeline_function.__name__ + '.pipeline.yaml')

TektonCompiler().compile(pipeline_function, pipeline_filename)

############################################################
#              Run the pipeline
############################################################

client = TektonClient(${pipeline_server})

# Get or create an experiment and submit a pipeline run
experiment = client.create_experiment('NOTEBOOK_RUNS')

# Submit the experiment to run in a pipeline
run_name = '${run_name}'
run_result = client.run_pipeline(experiment.id, run_name, pipeline_filename)
