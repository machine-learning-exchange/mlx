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
import swagger_client

from os import environ as env
from pprint import pprint
from swagger_client.api_client import ApiClient, Configuration
from swagger_client.models import ApiListCatalogItemsResponse, ApiCatalogUpload,\
    ApiCatalogUploadItem, ApiCatalogUploadResponse, ApiAccessToken
from swagger_client.rest import ApiException
from sys import stderr


host = '127.0.0.1'
port = '8080'
# host = env.get("MLX_API_SERVICE_HOST")
# port = env.get("MLX_API_SERVICE_PORT")

api_base_path = 'apis/v1alpha1'

catalog_upload_file = "./../../bootstrapper/catalog_upload.json"

IBM_GHE_API_TOKEN = env.get("IBM_GHE_API_TOKEN")


def get_swagger_client():

    config = Configuration()
    config.host = f'http://{host}:{port}/{api_base_path}'
    api_client = ApiClient(configuration=config)

    return api_client


def print_function_name_decorator(func):

    def wrapper(*args, **kwargs):
        print()
        print(f"---[ {func.__name__} ]---")
        print()
        return func(*args, **kwargs)

    return wrapper


@print_function_name_decorator
def upload_catalog_assets(upload_file=catalog_upload_file) -> ApiCatalogUploadResponse:

    api_client = get_swagger_client()
    api_instance = swagger_client.CatalogServiceApi(api_client=api_client)

    try:
        with open(upload_file) as f:
            upload_items = json.load(f)

        upload_body = ApiCatalogUpload(
            api_access_tokens=[ApiAccessToken(api_token=IBM_GHE_API_TOKEN, url_host="github.ibm.com")],
            components=upload_items.get("components"),
            datasets=upload_items.get("datasets"),
            models=upload_items.get("models"),
            notebooks=upload_items.get("notebooks"),
            pipelines=upload_items.get("pipelines"))

        upload_response: ApiCatalogUploadResponse = api_instance.upload_multiple_assets(upload_body)

        print(f"Uploaded '{upload_response.total_created}' assets, {upload_response.total_errors} errors")

        # print a short-ish table instead of the full JSON response
        asset_types = [
            "components",
            "datasets",
            "models",
            "notebooks",
            "pipelines"
        ]
        for asset_type in asset_types:
            asset_list = upload_response.__getattribute__(asset_type)
            print(f"\n{asset_type.upper()}:\n")
            for asset in asset_list:
                print("%s  %s  %s" % (asset.id, asset.created_at.strftime("%Y-%m-%d %H:%M:%S"), asset.name))

        if upload_response.total_errors > 0:
            print(f"\nERRORS:\n")
            for error in upload_response.errors:
                print(error.error_message)

        return upload_response

    except ApiException as e:
        print("Exception when calling CatalogServiceApi -> upload_multiple_assets: %s\n" % e, file=stderr)
        raise e

    return None


@print_function_name_decorator
def delete_assets(upload_assets_response: ApiCatalogUploadResponse = None):

    api_client = get_swagger_client()

    delete_methods = {
        "components": swagger_client.ComponentServiceApi(api_client).delete_component,
        "datasets": swagger_client.DatasetServiceApi(api_client).delete_dataset,
        "models": swagger_client.ModelServiceApi(api_client).delete_model,
        "notebooks": swagger_client.NotebookServiceApi(api_client).delete_notebook,
        "pipelines": swagger_client.PipelineServiceApi(api_client).delete_pipeline
    }

    try:
        for asset_type, delete_method in delete_methods.items():
            if upload_assets_response:
                asset_list = upload_assets_response.__getattribute__(asset_type)
                for asset in asset_list:
                    delete_method(asset.id)
            else:
                delete_method("*")

    except ApiException as e:
        print(f"Exception when calling {delete_method}: {e}\n", file=stderr)


@print_function_name_decorator
def list_assets(filter_dict: dict = {}, sort_by: str = None) -> ApiListCatalogItemsResponse:

    api_client = get_swagger_client()
    api_instance = swagger_client.CatalogServiceApi(api_client=api_client)

    try:
        filter_str = json.dumps(filter_dict) if filter_dict else None

        api_response: ApiListCatalogItemsResponse = \
            api_instance.list_all_assets(filter=filter_str, sort_by=sort_by)

        asset_types = [
            "components",
            "datasets",
            "models",
            "notebooks",
            "pipelines"
        ]

        # print a short-ish table instead of the full JSON response
        for asset_type in asset_types:
            asset_list = api_response.__getattribute__(asset_type)
            for asset in asset_list:
                print("%s  %s  %s" % (asset.id, asset.created_at.strftime("%Y-%m-%d %H:%M:%S"), asset.name))

        return api_response

    except ApiException as e:
        print("Exception when calling CatalogServiceApi -> list_all_assets: %s\n" % e, file=stderr)

    return []


def main():

    # delete all existing assets
    delete_assets()

    # upload the assets configured in the bootstrapper
    upload_response = upload_catalog_assets()

    # delete (only) the assets we just uploaded
    # delete_assets(upload_response)

    # list the remaining assets
    list_assets()


if __name__ == '__main__':
    main()
