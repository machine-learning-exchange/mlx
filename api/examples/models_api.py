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
import os
import random
import re
import swagger_client
import tarfile
import tempfile

from glob import glob
from io import BytesIO
from os import environ as env
from pprint import pprint
from swagger_client.api_client import ApiClient, Configuration
from swagger_client.models import ApiModel, ApiGetTemplateResponse, ApiListModelsResponse, \
    ApiGenerateModelCodeResponse, ApiRunCodeResponse
from swagger_client.rest import ApiException
from sys import stderr
from urllib3.response import HTTPResponse


host = '127.0.0.1'
port = '8080'
# host = env.get("MLX_API_SERVICE_HOST")
# port = env.get("MLX_API_SERVICE_PORT")

api_base_path = 'apis/v1alpha1'

yaml_files = glob("./../../models/samples/*.yaml")


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


def upload_model_template(uploadfile_name, name=None) -> str:
    api_client = get_swagger_client()
    api_instance = swagger_client.ModelServiceApi(api_client=api_client)
    try:
        print(f"Uploading '{uploadfile_name}' ... ", end='')
        model: ApiModel = api_instance.upload_model(uploadfile=uploadfile_name, name=name)
        print(f"{model.id} '{model.name}'")
        return model.id
    except ApiException as e:
        print("Exception when calling ModelServiceApi -> upload_model: %s\n" % e, file=stderr)
        raise e
    return None


@print_function_name_decorator
def upload_model_file(model_id, file_path):
    api_client = get_swagger_client()
    api_instance = swagger_client.ModelServiceApi(api_client=api_client)
    try:
        response = api_instance.upload_model_file(id=model_id, uploadfile=file_path)
        print(f"Upload file '{file_path}' to model '{model_id}'")
    except ApiException as e:
        print("Exception when calling ModelServiceApi -> upload_model_file: %s\n" % e, file=stderr)
        raise e


@print_function_name_decorator
def upload_model_templates(yaml_files=yaml_files) -> [str]:
    template_ids = []
    for yaml_file in yaml_files:
        # tarfile_name = create_tar_file(yaml_file)
        # template_id = upload_model_template(tarfile_name)
        template_id = upload_model_template(yaml_file)
        template_ids += [template_id]
    return template_ids


@print_function_name_decorator
def download_model_tgz(model_id, download_dir: str = None) -> str:

    api_client = get_swagger_client()
    api_instance = swagger_client.ModelServiceApi(api_client=api_client)

    try:
        response: HTTPResponse = \
            api_instance.download_model_files(model_id,
                                              include_generated_code=True,
                                              _preload_content=False)

        attachment_header = response.info().get("Content-Disposition",
                                                f"attachment; filename={model_id}.tgz")

        download_filename = re.sub("attachment; filename=", "", attachment_header)

        download_dir = download_dir or os.path.join(tempfile.gettempdir(), "download", "models")
        os.makedirs(download_dir, exist_ok=True)
        tarfile_path = os.path.join(download_dir, download_filename)

        with open(tarfile_path, 'wb') as f:
            f.write(response.read())

        print(tarfile_path)

        return tarfile_path

    except ApiException as e:
        print("Exception when calling ModelServiceApi -> download_model_files: %s\n" % e, file=stderr)

    return "Download failed?"


@print_function_name_decorator
def verify_model_download(model_id: str) -> bool:

    api_client = get_swagger_client()
    api_instance = swagger_client.ModelServiceApi(api_client=api_client)

    try:
        response: HTTPResponse = \
            api_instance.download_model_files(model_id,
                                              include_generated_code=True,
                                              _preload_content=False)
        tgz_file = BytesIO(response.read())
        tar = tarfile.open(fileobj=tgz_file)

        file_contents = {m.name: tar.extractfile(m).read().decode("utf-8")
                         for m in tar.getmembers()}

        # verify template text matches

        template_response: ApiGetTemplateResponse = api_instance.get_model_template(model_id)
        template_from_api = template_response.template
        template_from_tgz = [content for filename, content in file_contents.items()
                             if filename.endswith(".yaml") or filename.endswith(".yml")][0]

        assert template_from_api == template_from_tgz

        # verify generated code matches

        generate_code_response: ApiGenerateModelCodeResponse = \
            api_instance.generate_model_code(model_id)

        for model_script in generate_code_response.scripts:
            stage = model_script.pipeline_stage
            platform = model_script.execution_platform
            script_from_api = model_script.script_code

            downloaded_script = [content for filename, content in file_contents.items()
                                 if f"run_{stage}_{platform}" in filename][0]

            assert script_from_api == downloaded_script

        print("downloaded files match")

        return True

    except ApiException as e:
        print("Exception when calling ModelServiceApi -> download_model_files: %s\n" % e, file=stderr)

    return False


@print_function_name_decorator
def approve_models_for_publishing(model_ids: [str]):

    api_client = get_swagger_client()
    api_instance = swagger_client.ModelServiceApi(api_client=api_client)

    try:
        api_response = api_instance.approve_models_for_publishing(model_ids)

    except ApiException as e:
        print("Exception when calling ModelServiceApi -> approve_models_for_publishing: %s\n" % e, file=stderr)

    return None


@print_function_name_decorator
def set_featured_models(model_ids: [str]):

    api_client = get_swagger_client()
    api_instance = swagger_client.ModelServiceApi(api_client=api_client)

    try:
        api_response = api_instance.set_featured_models(model_ids)

    except ApiException as e:
        print("Exception when calling ModelServiceApi -> set_featured_models: %s\n" % e, file=stderr)

    return None


@print_function_name_decorator
def get_model(model_id: str) -> ApiModel:
    api_client = get_swagger_client()
    api_instance = swagger_client.ModelServiceApi(api_client=api_client)
    try:
        model_meta: ApiModel = api_instance.get_model(model_id)
        pprint(model_meta, indent=2)
        return model_meta
    except ApiException as e:
        print("Exception when calling ModelServiceApi -> get_model: %s\n" % e, file=stderr)
    return None


@print_function_name_decorator
def delete_model(model_id: str):
    api_client = get_swagger_client()
    api_instance = swagger_client.ModelServiceApi(api_client=api_client)
    try:
        api_instance.delete_model(model_id)
    except ApiException as e:
        print("Exception when calling ModelServiceApi -> delete_model: %s\n" % e, file=stderr)


@print_function_name_decorator
def get_template(template_id: str) -> str:

    api_client = get_swagger_client()
    api_instance = swagger_client.ModelServiceApi(api_client=api_client)

    try:
        template_response: ApiGetTemplateResponse = api_instance.get_model_template(template_id)
        print(template_response.template)

        # yaml_dict = yaml.load(template_response.template, Loader=yaml.FullLoader)
        # model_name = yaml_dict.get("name") or f"template_{template_id}"
        # template_file = os.path.join("files", model_name) + ".yaml"

        # with open(template_file, "w") as f:
        #     f.write(template_response.template)

        return template_response.template

    except ApiException as e:
        print("Exception when calling ModelServiceApi -> get_model_template: %s\n" % e, file=stderr)

    return None


@print_function_name_decorator
def generate_code(model_id: str) -> str:

    api_client = get_swagger_client()
    api_instance = swagger_client.ModelServiceApi(api_client=api_client)

    try:
        generate_code_response: ApiGenerateModelCodeResponse = api_instance.generate_model_code(model_id)

        for model_script in generate_code_response.scripts:
            print(f"#######################################################")
            print(f"# pipeline_stage:     {model_script.pipeline_stage}")
            print(f"# execution_platform: {model_script.execution_platform}")
            print(f"#######################################################")
            print()
            print(model_script.script_code)
            print()

        return generate_code_response.scripts

    except ApiException as e:
        print("Exception while calling ModelServiceApi -> generate_code: %s\n" % e, file=stderr)

    return None


@print_function_name_decorator
def run_code(model_id: str, pipeline_stage: str, execution_platform: str, run_name: str = None, parameters=dict()) -> str:

    api_client = get_swagger_client()
    api_instance = swagger_client.ModelServiceApi(api_client=api_client)

    try:
        run_code_response: ApiRunCodeResponse = api_instance.run_model(model_id, pipeline_stage, execution_platform,
                                                                       run_name=run_name, parameters=parameters)
        print(run_code_response.run_url)

        return run_code_response.run_url

    except ApiException as e:
        print("Exception while calling ModelServiceApi -> run_code: %s\n" % e, file=stderr)

    return None


@print_function_name_decorator
def list_models(filter_dict: dict = {}, sort_by: str = None) -> [ApiModel]:

    api_client = get_swagger_client()
    api_instance = swagger_client.ModelServiceApi(api_client=api_client)

    try:
        filter_str = json.dumps(filter_dict) if filter_dict else None

        api_response: ApiListModelsResponse = api_instance.list_models(filter=filter_str, sort_by=sort_by)

        for c in api_response.models:
            print("%s  %s  %s" % (c.id, c.created_at.strftime("%Y-%m-%d %H:%M:%S"), c.name))

        return api_response.models

    except ApiException as e:
        print("Exception when calling ModelServiceApi -> list_models: %s\n" % e, file=stderr)

    return []


def main():
    # delete existing models
    delete_model(model_id="*")

    # upload all templates
    model_ids: [str] = upload_model_templates()

    # list all models
    models = list_models()
    model_ids: [str] = [model.id for model in models]

    # set featured models
    set_featured_models(model_ids)

    # approve models to be published
    approve_models_for_publishing(model_ids)

    # randomly selected a model
    i = random.randint(0, len(model_ids)-1)
    model_id = model_ids[i]

    # show one randomly selected model, gen code, download, update
    get_model(model_id)
    generate_code(model_id)
    get_template(model_id)
    tarfile_path = download_model_tgz(model_id)
    verify_model_download(model_id)
    upload_model_file(model_id, tarfile_path)

    # run code
    model = get_model("max-image-caption-generator")
    get_template(model.id)
    generate_code(model.id)
    run_code(model.id, "serve", "kubernetes", "Maximum image captioning fun")

    # model_id = upload_model_templates(["./temp/models/max-image-completer.yaml"])[0]
    # verify_model_download(model_id)
    # run_code(model_id, "train", "WatsonML")
    # delete_model(model_id)

    # # update existing model
    # model = get_model("max-audio-classifier")
    # upload_model_file(model.id, "temp/files/max-audio-classifier.tgz")
    # upload_model_file(model.id, "temp/files/max-audio-classifier.yaml")


if __name__ == '__main__':
    main()
