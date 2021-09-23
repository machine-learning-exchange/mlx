#!/usr/bin/env python3

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

from __future__ import print_function

import json
import yaml

from glob import glob
from os.path import abspath, dirname, relpath


asset_types = [
    "component",
    "dataset",
    "model",
    "notebook",
    "pipeline",
]

script_path = abspath(dirname(__file__))
project_dir = dirname(script_path)

katalog_dir = f"{project_dir}/../katalog"  # TODO: don't assume user cloned katalog and mlx repos into same parent folder
katalog_url = "https://raw.githubusercontent.com/machine-learning-exchange/katalog/main/"

catalog_upload_json_files = [
    f"{project_dir}/bootstrapper/catalog_upload.json",
    f"{project_dir}/quickstart/catalog_upload.json",
]


def get_list_of_yaml_files_in_katalog(asset_type: str):

    yaml_files = glob(f"{katalog_dir}/{asset_type}-samples/**/*.yaml", recursive=True)

    yaml_files = [filepath for filepath in yaml_files
                  if not any(word in filepath for word in ["template", "test", "src"])]

    return sorted(yaml_files)


def generate_katalog_dict() -> dict:

    katalog_dict = dict()

    for asset_type in asset_types:

        yaml_files = get_list_of_yaml_files_in_katalog(asset_type)
        katalog_asset_list = []

        for yaml_file in yaml_files:

            with open(yaml_file) as f:
                yaml_dict = yaml.load(f, Loader=yaml.FullLoader)
                asset_name = yaml_dict.get("name") or \
                             yaml_dict.get("metadata", {}).get("name", "").replace("-", " ").title() \
                             or ""
                asset_url = katalog_url + relpath(yaml_file, katalog_dir)

            katalog_asset_item = {
                "name": asset_name,
                "url": asset_url
            }

            katalog_asset_list.append(katalog_asset_item)

        katalog_dict[asset_type + "s"] = katalog_asset_list

    return katalog_dict


def rewrite_catalog_upload_json_files(katalog: dict):

    for file_path in catalog_upload_json_files:

        with open(file_path, "w") as output_file:

            print(" - " + relpath(file_path, project_dir))

            output_file.write(json.dumps(katalog, sort_keys=False, indent=2))
            output_file.write("\n")


def main():

    print("Regenerating catalog_upload.json files:")

    # TODO: read current catalog_upload.json file(s) to capture non-katalog assets and restore later

    katalog_dict = generate_katalog_dict()

    rewrite_catalog_upload_json_files(katalog_dict)

    print("Done. Use git diff to evaluate if and which changes are desired!")


if __name__ == '__main__':

    main()
