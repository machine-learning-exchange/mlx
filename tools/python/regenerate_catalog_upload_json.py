#!/usr/bin/env python3

# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import print_function

import difflib
import json
import yaml
import os

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
project_dir = dirname(dirname(script_path))

katalog_dir = f"{project_dir}/../katalog"
katalog_url = "https://raw.githubusercontent.com/machine-learning-exchange/katalog/main/"

catalog_upload_json_files = [
    f"{project_dir}/bootstrapper/catalog_upload.json",
    # f"{project_dir}/quickstart/catalog_upload.json",
]


def get_list_of_yaml_files_in_katalog(asset_type: str):

    yaml_files = glob(f"{katalog_dir}/{asset_type}-samples/**/*.yaml", recursive=True)

    yaml_files = [filepath for filepath in yaml_files
                  if not any(word in filepath for word in ["template", "test", "src"])]

    return sorted(yaml_files)


def generate_katalog_dict() -> dict:

    katalog_dict = dict()
    if not (os.path.isdir(katalog_dir)):
        os.chdir(f"{project_dir}/..")
        os.system("git clone https://github.com/machine-learning-exchange/katalog.git")

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

        print(" - " + relpath(file_path, project_dir))

        with open(file_path, "r") as target_file:

            json_dict = json.load(target_file)
            for element in json_dict:
                if element[0: -1] not in asset_types:
                    katalog[element] = json_dict[element]

        with open(file_path, "w") as output_file:

            output_file.write(json.dumps(katalog, sort_keys=False, indent=2))
            output_file.write("\n")

        print('Please evaluate the changes:')

        for line in difflib.unified_diff(
            json.dumps(json_dict, sort_keys=True, indent=2).split("\n"), json.dumps(katalog, sort_keys=True, indent=2).split("\n"), lineterm=''):
            print(line)

def main():

    print("Regenerating catalog_upload.json files:")

    katalog_dict = generate_katalog_dict()

    rewrite_catalog_upload_json_files(katalog_dict)

    print("Done. Use git diff to evaluate if and which changes are desired!")


if __name__ == '__main__':

    main()
