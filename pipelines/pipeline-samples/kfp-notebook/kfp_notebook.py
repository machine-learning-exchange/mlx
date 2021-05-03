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

import os
import kfp
import kfp.dsl as dsl
from kfp_notebook.pipeline import NotebookOp
from kfp_tekton.compiler import TektonCompiler
from kubernetes.client.models import V1EnvVar

# KubeFlow Pipelines API Endpoint
kfp_url = 'http://x.x.x.x:31380/pipeline/'

# S3 Object Storage Endpoint and Credentials
cos_endpoint = 'http://s3.xxx'
cos_bucket = 'bucket_name'
cos_username = 'username'
cos_password = 'password'
cos_directory = 'directory'

# Name of compressed folder containing runtime dependencies for this pipeline.
# Push to cos before running the pipeline.
cos_dependencies_archive = 'notebook.tar.gz'

# Inputs and Outputs
inputs = []
outputs = []

# Container Image
image = 'tensorflow/tensorflow:latest'

def run_notebook_op(op_name):
    
    notebook_op = NotebookOp(name=op_name,
                            notebook='Untitled.ipynb',
                             cos_endpoint=cos_endpoint,
                             cos_bucket=cos_bucket,
                             cos_directory=cos_directory,
                             cos_dependencies_archive=cos_dependencies_archive,
                             pipeline_outputs=outputs,
                             pipeline_inputs=inputs,
                             image=image)

    notebook_op.container.add_env_variable(V1EnvVar(name='AWS_ACCESS_KEY_ID', value=cos_username))
    notebook_op.container.add_env_variable(V1EnvVar(name='AWS_SECRET_ACCESS_KEY', value=cos_password))
    notebook_op.container.set_image_pull_policy('Always')
    return notebook_op

@dsl.pipeline(
  name='Sample kfp notebook pipeline',
  description='Sample template to compile and export a kfp notebook'
)
def demo_pipeline():
    run_notebook_op('dummy_name')

# Compile the new pipeline
TektonCompiler().compile(demo_pipeline, 'pipeline.tar.gz')

# Upload the compiled pipeline
client = kfp.Client(host=kfp_url)
pipeline_info = client.upload_pipeline('pipeline.tar.gz',pipeline_name='pipeline-demo')

# Create a new experiment
experiment = client.create_experiment(name='demo-experiment')

# Create a new run associated with experiment and our uploaded pipeline
run = client.run_pipeline(experiment.id, 'demo-run', pipeline_id=pipeline_info.id)