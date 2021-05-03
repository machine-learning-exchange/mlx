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
import argparse
import os
import yaml

from metadata_converter.generate import generate_dlf_yaml, generate_dlf_yaml_dict
from urllib.parse import urlparse
from urllib.request import urlopen


def is_url(url):
  try:
    result = urlparse(url)
    return all([result.scheme, result.netloc])
  except ValueError:
    return False


# python dataset_converter.py \
#    --dataset-yaml "$(cat ~/Projects/metadata-converter/dax-data-set-descriptors/jfk.yaml)" \
#    --output-path /tmp/jfk-dlf.yaml
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--dataset-yaml",
        type=str,
        help="Dataset YAML (string-serialized) or a URL pointing to YAML file in Data Asset Exchange format",
        required=True
    )
    parser.add_argument(
        "-o", "--output-path",
        type=str,
        help="Path to store output YAML in Dataset Lifecycle Framework YAML format",
        default="/tmp/output"
    )
    args = parser.parse_args()
    dataset_yaml = args.dataset_yaml
    output_path = args.output_path

    if is_url(dataset_yaml):
        response = urlopen(url=dataset_yaml)
        dax_yaml = yaml.safe_load(response.read())
    else:
        dax_yaml = yaml.safe_load(dataset_yaml)

    dlf_yaml = generate_dlf_yaml(dax_yaml)

    if os.path.dirname(output_path) and \
            not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))

    with open(output_path, "w") as f:
        f.write(dlf_yaml)

    print("Successfully generated DLF YAML file: " + os.path.abspath(output_path))
