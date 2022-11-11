# Copyright 2021 The MLX Contributors
# 
# SPDX-License-Identifier: Apache-2.0

from __future__ import print_function

import glob
import json
import os
import random
import re
import swagger_client
import tarfile
import tempfile

from io import BytesIO
from os import environ as env
from pprint import pprint
from swagger_client.api_client import ApiClient, Configuration
from swagger_client.models import ApiComponent, ApiGetTemplateResponse, ApiListComponentsResponse, \
    ApiGenerateCodeResponse, ApiRunCodeResponse
from swagger_client.rest import ApiException
from sys import stderr
from urllib3.response import HTTPResponse


host = '127.0.0.1'
port = '8080'
# host = env.get("MLX_API_SERVICE_HOST")
# port = env.get("MLX_API_SERVICE_PORT")

api_base_path = 'apis/v1alpha1'

yaml_files = glob.glob("./../../../katalog/component-samples/**/component.yaml", recursive=True)


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


def create_tar_file(yamlfile_name):

    yamlfile_basename = os.path.basename(yamlfile_name)
    tmp_dir = tempfile.gettempdir()
    tarfile_path = os.path.join(tmp_dir, yamlfile_basename.replace(".yaml", ".tgz"))

    with tarfile.open(tarfile_path, "w:gz") as tar:
        tar.add(yamlfile_name, arcname=yamlfile_basename)

    tar.close()

    return tarfile_path


def upload_component_template(uploadfile_name, name=None) -> str:

    api_client = get_swagger_client()
    api_instance = swagger_client.ComponentServiceApi(api_client=api_client)

    try:
        component: ApiComponent = api_instance.upload_component(uploadfile=uploadfile_name, name=name)
        print(f"Uploaded '{component.name}': {component.id}")
        return component.id

    except ApiException as e:
        print("Exception when calling ComponentServiceApi -> upload_component: %s\n" % e, file=stderr)
        raise e

    return None


@print_function_name_decorator
def upload_component_templates() -> [str]:

    template_ids = []

    for yaml_file in yaml_files:
        # tarfile_name = create_tar_file(yaml_file)
        # template_id = upload_component_template(tarfile_name)
        template_id = upload_component_template(yaml_file)
        template_ids += [template_id]

    return template_ids


@print_function_name_decorator
def upload_component_file(component_id, file_path):

    api_client = get_swagger_client()
    api_instance = swagger_client.ComponentServiceApi(api_client=api_client)

    try:
        response = api_instance.upload_component_file(id=component_id, uploadfile=file_path)
        print(f"Upload file '{file_path}' to component with ID '{component_id}'")

    except ApiException as e:
        print("Exception when calling ComponentServiceApi -> upload_component_file: %s\n" % e, file=stderr)
        raise e


@print_function_name_decorator
def download_component_tgz(component_id) -> str:

    api_client = get_swagger_client()
    api_instance = swagger_client.ComponentServiceApi(api_client=api_client)

    try:
        response: HTTPResponse = \
            api_instance.download_component_files(component_id,
                                                  include_generated_code=True,
                                                  _preload_content=False)

        attachment_header = response.info().get("Content-Disposition",
                                                f"attachment; filename={component_id}.tgz")

        download_filename = re.sub("attachment; filename=", "", attachment_header)

        download_dir = os.path.join(tempfile.gettempdir(), "download", "components")
        os.makedirs(download_dir, exist_ok=True)
        tarfile_path = os.path.join(download_dir, download_filename)

        with open(tarfile_path, 'wb') as f:
            f.write(response.read())

        print(tarfile_path)

        return tarfile_path

    except ApiException as e:
        print("Exception when calling ComponentServiceApi -> download_component_files: %s\n" % e, file=stderr)

    return "Download failed?"


@print_function_name_decorator
def verify_component_download(component_id: str) -> bool:

    api_client = get_swagger_client()
    api_instance = swagger_client.ComponentServiceApi(api_client=api_client)

    try:
        response: HTTPResponse = \
            api_instance.download_component_files(component_id,
                                                  include_generated_code=True,
                                                  _preload_content=False)
        tgz_file = BytesIO(response.read())
        tar = tarfile.open(fileobj=tgz_file)

        file_contents = {m.name.split(".")[-1]: tar.extractfile(m).read().decode("utf-8")
                         for m in tar.getmembers()}

        template_response: ApiGetTemplateResponse = api_instance.get_component_template(component_id)
        template_text_from_api = template_response.template

        assert template_text_from_api == file_contents.get("yaml", file_contents.get("yml"))

        generate_code_response: ApiGenerateCodeResponse = api_instance.generate_component_code(component_id)
        run_script_from_api = generate_code_response.script

        regex = re.compile(r"name='[^']*'")  # controller adds random chars to name, replace those

        assert regex.sub("name='...'", run_script_from_api) == \
               regex.sub("name='...'", file_contents.get("py"))

        print("downloaded files match")

        return True

    except ApiException as e:
        print("Exception when calling ComponentServiceApi -> download_component_files: %s\n" % e, file=stderr)

    return False


@print_function_name_decorator
def approve_components_for_publishing(component_ids: [str]):

    api_client = get_swagger_client()
    api_instance = swagger_client.ComponentServiceApi(api_client=api_client)

    try:
        api_response = api_instance.approve_components_for_publishing(component_ids)

    except ApiException as e:
        print("Exception when calling ComponentServiceApi -> approve_components_for_publishing: %s\n" % e, file=stderr)

    return None


@print_function_name_decorator
def set_featured_components(component_ids: [str]):

    api_client = get_swagger_client()
    api_instance = swagger_client.ComponentServiceApi(api_client=api_client)

    try:
        api_response = api_instance.set_featured_components(component_ids)

    except ApiException as e:
        print("Exception when calling ComponentServiceApi -> set_featured_components: %s\n" % e, file=stderr)

    return None


@print_function_name_decorator
def get_component(component_id: str) -> ApiComponent:

    api_client = get_swagger_client()
    api_instance = swagger_client.ComponentServiceApi(api_client=api_client)

    try:
        component_meta: ApiComponent = api_instance.get_component(component_id)
        pprint(component_meta, indent=2)
        return component_meta

    except ApiException as e:
        print("Exception when calling ComponentServiceApi -> get_component: %s\n" % e, file=stderr)

    return None


@print_function_name_decorator
def delete_component(component_id: str):

    api_client = get_swagger_client()
    api_instance = swagger_client.ComponentServiceApi(api_client=api_client)

    try:
        api_instance.delete_component(component_id)
    except ApiException as e:
        print("Exception when calling ComponentServiceApi -> delete_component: %s\n" % e, file=stderr)


@print_function_name_decorator
def get_template(template_id: str) -> str:

    api_client = get_swagger_client()
    api_instance = swagger_client.ComponentServiceApi(api_client=api_client)

    try:
        template_response: ApiGetTemplateResponse = api_instance.get_component_template(template_id)
        print(template_response.template)

        # yaml_dict = yaml.load(template_response.template, Loader=yaml.FullLoader)
        # component_name = yaml_dict.get("name") or f"template_{template_id}"
        # template_file = os.path.join("files", component_name) + ".yaml"

        # with open(template_file, "w") as f:
        #     f.write(template_response.template)

        return template_response.template

    except ApiException as e:
        print("Exception when calling ComponentServiceApi -> get_component_template: %s\n" % e, file=stderr)

    return None


@print_function_name_decorator
def generate_code(component_id: str) -> str:

    api_client = get_swagger_client()
    api_instance = swagger_client.ComponentServiceApi(api_client=api_client)

    try:
        generate_code_response: ApiGenerateCodeResponse = api_instance.generate_component_code(component_id)
        print(generate_code_response.script)

        return generate_code_response.script

    except ApiException as e:
        print("Exception while calling ComponentServiceApi -> generate_code: %s\n" % e, file=stderr)

    return None


@print_function_name_decorator
def run_code(component_id: str, parameters: dict = {}, run_name: str = None) -> str:

    api_client = get_swagger_client()
    api_instance = swagger_client.ComponentServiceApi(api_client=api_client)

    try:
        param_array = [{"name": key, "value": value} for key, value in parameters.items()]
        run_code_response: ApiRunCodeResponse = api_instance.run_component(component_id, param_array, run_name=run_name)
        print(run_code_response.run_url)

        return run_code_response.run_url

    except ApiException as e:
        print("Exception while calling ComponentServiceApi -> run_code: %s\n" % e, file=stderr)

    return None


@print_function_name_decorator
def list_components(filter_dict: dict = {}, sort_by: str = None) -> [ApiComponent]:

    api_client = get_swagger_client()
    api_instance = swagger_client.ComponentServiceApi(api_client=api_client)

    try:
        filter_str = json.dumps(filter_dict) if filter_dict else None

        api_response: ApiListComponentsResponse = api_instance.list_components(filter=filter_str, sort_by=sort_by)

        for c in api_response.components:
            print("%s  %s  %s" % (c.id, c.created_at.strftime("%Y-%m-%d %H:%M:%S"), c.name))

        return api_response.components

    except ApiException as e:
        print("Exception when calling ComponentServiceApi -> list_components: %s\n" % e, file=stderr)

    return []


def main():
    # delete existing components
    delete_component(component_id="*")

    # upload all templates
    component_ids: [str] = upload_component_templates()

    # list all components
    components = list_components()
    component_ids: [str] = [component.id for component in components]

    # set featured components
    set_featured_components(component_ids)

    # approve components to be published
    approve_components_for_publishing(component_ids)

    # randomly selected a component
    i = random.randint(0, len(component_ids)-1)
    component_id = component_ids[i]

    # show one randomly selected component
    get_component(component_id)
    get_template(component_id)
    generate_code(component_id)

    tgz_file = download_component_tgz(component_id)
    verify_component_download(component_id)
    upload_component_file(component_id, tgz_file)

    component = list_components(filter_dict={"name": 'Create Secret - Kubernetes Cluster'})[0]
    generate_code(component.id)
    args = {
        'token': env.get("GHE_API_TOKEN"),
        'url': 'https://raw.github.ibm.com/user/repo/master/secret.yml',
        'name': 'my-test-credential'
    }
    run_code(component.id, args, f"Running component '{component.id}'")

    # # delete one component
    # delete_component(component_id)
    
    # # update a component
    # component = list_components(filter_dict={"name": 'Fabric for Deep Learning - Train Model'})[0]
    # update_component_template(component.id, "temp/files/ffdl_train.yaml")


if __name__ == '__main__':
    main()
