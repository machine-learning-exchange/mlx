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
import kfp
from kfp import components
import yaml

dlf_op = components.load_component_from_file('component.yaml')

with open("dlf_example.yaml", 'r') as stream:
    sample_dlf = yaml.safe_load(stream)

@dsl.pipeline(
  name='dlf',
  description='A pipeline for dfl'
)
def dlfPipeline(
    action='create',
    dataset_yaml=yaml.safe_dump(sample_dlf)
):

    # define workflow
    dlf = dlf_op(action=action,
                 dataset_yaml=dataset_yaml).set_image_pull_policy('Always')

# Compile pipeline
from kfp_tekton.compiler import TektonCompiler
TektonCompiler().compile(dlfPipeline, 'dlf.yaml')
