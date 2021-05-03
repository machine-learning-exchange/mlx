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
import random
import swagger_client

from os import environ as env
from pprint import pprint
from pipelines_api import list_pipelines
from swagger_client.api_client import ApiClient, Configuration
from swagger_client.models import ApiCredential, ApiListCredentialsResponse
from swagger_client.rest import ApiException
from sys import stderr
from urllib3.response import HTTPResponse


host = '127.0.0.1'
port = '8080'
# host = env.get("MLX_API_SERVICE_HOST")
# port = env.get("MLX_API_SERVICE_PORT")

api_base_path = 'apis/v1alpha1'


def get_swagger_client():

    config = Configuration()
    config.host = f'http://{host}:{port}/{api_base_path}'
    api_client = ApiClient(configuration=config)

    return api_client


def print_function_name_decorator(func):

    def wrapper(*args, **kwargs):
        print()
        print(f"---[ {func.__name__}{args}{kwargs} ]---")
        print()
        return func(*args, **kwargs)

    return wrapper


@print_function_name_decorator
def create_credential(pipeline_id: str, project_id: str, data_assets: [str] = []) -> ApiCredential:

    api_client = get_swagger_client()
    api_instance = swagger_client.CredentialServiceApi(api_client=api_client)

    try:
        api_credential = ApiCredential(pipeline_id=pipeline_id, project_id=project_id, data_assets=data_assets)

        api_response: ApiCredential = api_instance.create_credential(api_credential)

        return api_response

    except ApiException as e:
        print("Exception when calling CredentialServiceApi -> create_credential: %s\n" % e, file=stderr)

    return []


@print_function_name_decorator
def get_credential(credential_id: str) -> ApiCredential:

    api_client = get_swagger_client()
    api_instance = swagger_client.CredentialServiceApi(api_client=api_client)

    try:
        api_credential: ApiCredential = api_instance.get_credential(credential_id)
        pprint(api_credential, indent=2)
        return api_credential

    except ApiException as e:
        print("Exception when calling CredentialServiceApi -> get_credential: %s\n" % e, file=stderr)

    return None


@print_function_name_decorator
def delete_credential(credential_id: str):

    api_client = get_swagger_client()
    api_instance = swagger_client.CredentialServiceApi(api_client=api_client)

    try:
        api_instance.delete_credential(credential_id)
    except ApiException as e:
        print("Exception when calling CredentialServiceApi -> delete_credential: %s\n" % e, file=stderr)


@print_function_name_decorator
def list_credentials(filter_dict: dict = {}, sort_by: str = None) -> [ApiCredential]:

    api_client = get_swagger_client()
    api_instance = swagger_client.CredentialServiceApi(api_client=api_client)

    try:
        filter_str = json.dumps(filter_dict) if filter_dict else None

        api_response: ApiListCredentialsResponse = api_instance.list_credentials(filter=filter_str, sort_by=sort_by)

        for c in api_response.credentials:
            print("%s  %s  pl:%s  pr:%s" % (c.id, c.created_at.strftime("%Y-%m-%d %H:%M:%S"), c.pipeline_id, c.project_id))

        return api_response.credentials

    except ApiException as e:
        print("Exception when calling CredentialServiceApi -> list_credentials: %s\n" % e, file=stderr)

    return []


def main():
    # select a random pipeline
    pipelines = list_pipelines()
    i = random.randint(0, len(pipelines)-1)

    # create a new credential
    credential = create_credential(pipeline_id=pipelines[i].id, project_id="xyz", data_assets=["data1", "data2"])
    pprint(credential)

    # list credentials
    list_credentials()

    # list credentials for a pipeline
    list_credentials(filter_dict={"pipeline_id": pipelines[i].id})

    # retrieve credential
    credential = get_credential(credential.id)
    # pprint(credential)

    # delete credentials
    delete_credential(credential.id)


if __name__ == '__main__':
    # delete_credential("*")
    main()
