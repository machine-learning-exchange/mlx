#!/usr/bin/env python3

# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0

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

catalog_upload_json = "bootstrapper/catalog_upload.json"


def get_list_of_yaml_files_in_katalog(asset_type: str):

    yaml_files = glob(f"{katalog_dir}/{asset_type}-samples/**/*.yaml", recursive=True)

    yaml_files = [filepath for filepath in yaml_files
                  if not any(word in filepath for word in ["template", "test", "src"])]

    return sorted(yaml_files)


def generate_katalog_dict() -> dict:

    katalog_dict = {}

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


def rewrite_catalog_upload_json(katalog: dict):

    with open(f"{project_dir}/{catalog_upload_json}", "w") as output_file:

        print(f" - {catalog_upload_json}")

        output_file.write(json.dumps(katalog, sort_keys=False, indent=2))
        output_file.write("\n")


if __name__ == "__main__":

    print("Regenerating catalog_upload.json:")

    # TODO: read current catalog_upload.json file to capture non-katalog assets and restore later

    # Generate new catalog_upload.json
    rewrite_catalog_upload_json(generate_katalog_dict())

    print("Done. Use git diff to evaluate if and which changes are desired!")
