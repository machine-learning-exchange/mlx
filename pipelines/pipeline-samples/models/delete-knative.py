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
import ai_pipeline_params as params
import json

secret_name = 'e2e-creds'

@dsl.pipeline(
  name='Delete Knative pipeline',
  description='A pipeline for deleting serving models on knative.'
)
def deleteKnativePipeline(
    deployment_name='model-serving'
):

    """A pipeline to cleanup Knative Deployment."""

    delete_knative = dsl.ContainerOp(
         name='delete_knative_deployment',
         image='aipipeline/deployment-knative-remote',
         command=['sh', '-c'],
         arguments=['python -u knative_deployment.py --cleanup True --deployment_name %s' % (deployment_name)],
         file_outputs={'output': '/tmp/log.txt'}).apply(params.use_ai_pipeline_params(secret_name))


if __name__ == '__main__':
    import kfp.compiler as compiler
    compiler.Compiler().compile(deleteKnativePipeline, __file__ + '.tar.gz')
