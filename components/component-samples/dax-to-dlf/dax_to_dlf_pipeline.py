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
import yaml

from kfp import components
from kfp import dsl


dax_to_dlf_op = components.load_component_from_file('component.yaml')


def echo_op(text):
    return dsl.ContainerOp(
        name='echo',
        image='library/bash:4',
        command=['sh', '-c'],
        arguments=['echo "$0"', text]
    )


with open("dax_example.yaml", 'r') as stream:
    dax_example = yaml.safe_load(stream)


# https://developer.ibm.com/components/data-asset-exchange/data/
# https://github.com/CODAIT/exchange-metadata-converter/blob/main/templates/mlx_out.yaml
# https://github.com/IBM/dataset-lifecycle-framework
@dsl.pipeline(
    name='dax-to-dlf',
    description='Convert a Data Asset EXchange YAML file to Data Lifecycle Framework YAML file.'
)
def dax_to_dlf_pipeline(
    dax_yaml=yaml.safe_dump(dax_example)
):
    dax_to_dlf = dax_to_dlf_op(dax_yaml=dax_yaml)  # .set_image_pull_policy('Always')
    echo_op(dax_to_dlf.outputs["dlf_yaml"])


if __name__ == '__main__':
    from kfp_tekton.compiler import TektonCompiler
    TektonCompiler().compile(dax_to_dlf_pipeline, 'dax_to_dlf_pipeline.yaml')
