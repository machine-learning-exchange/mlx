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
import kfp.dsl as dsl
from kfp import components
import json

@dsl.pipeline(
  name='Notebook Execution pipeline',
  description='A pipeline for Notebook execution using papermill.'
)
def notebookPipeline(
    notebook_url='',
    notebook_params='',
    api_token='',
    endpoint_url='minio-service:9000',
    bucket_name='',
    access_key='minio',
    secret_access_key='minio123',
    object_name=''
):

    """A pipeline for notebook execution."""

    # define workflow
    notebook_execution = dsl.ContainerOp(
     name='notebook_execution',
     image='aipipeline/notebook-execution:latest',
     command=['python'],
     arguments=["-u", "execute_notebook.py",
                "--notebook_url", notebook_url,
                "--notebook_params", notebook_params,
                "--api_token", api_token,
                "--endpoint_url", endpoint_url,
                "--bucket_name", bucket_name,
                "--access_key", access_key,
                "--secret_access_key", secret_access_key,
                "--object_name", object_name
                ]
            )


if __name__ == '__main__':
    import kfp.compiler as compiler
    compiler.Compiler().compile(notebookPipeline, __file__ + '.tar.gz')
