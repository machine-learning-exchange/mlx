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
from swagger_client.models import ApiDataset, ApiGetTemplateResponse, ApiListDatasetsResponse, \
    ApiGenerateCodeResponse, ApiRunCodeResponse
from swagger_client.rest import ApiException
from sys import stderr
from urllib3.response import HTTPResponse

host = '127.0.0.1'
port = '8080'
# host = env.get("MLX_API_SERVICE_HOST")
# port = env.get("MLX_API_SERVICE_PORT")

api_base_path = 'apis/v1alpha1'

yaml_files = sorted(filter(lambda f: "lorem_ipsum" not in f, glob("./../../../katalog/dataset-samples/*.yaml")))


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
    # TODO: change how to get the basename after adding real dataset samples
    yamlfile_basename = "{}.yaml".format(yamlfile_name.split(os.path.sep)[-3])
    tmp_dir = tempfile.gettempdir()
    tarfile_path = os.path.join(tmp_dir, yamlfile_basename.replace(".yaml", ".tgz"))

    with tarfile.open(tarfile_path, "w:gz") as tar:
        tar.add(yamlfile_name, arcname=yamlfile_basename)

    tar.close()

    return tarfile_path


def upload_dataset_template(uploadfile_name, name=None) -> str:
    api_client = get_swagger_client()
    api_instance = swagger_client.DatasetServiceApi(api_client=api_client)

    try:
        dataset: ApiDataset = api_instance.upload_dataset(uploadfile=uploadfile_name, name=name)
        print(f"Uploaded '{dataset.name}': {dataset.id}")
        return dataset.id

    except ApiException as e:
        print("Exception when calling DatasetServiceApi -> upload_dataset: %s\n" % e, file=stderr)
        # raise e

    return None


@print_function_name_decorator
def upload_dataset_templates() -> [str]:
    template_ids = []

    for yaml_file in yaml_files:
        # tarfile_name = create_tar_file(yaml_file)
        # template_id = upload_dataset_template(tarfile_name)
        template_id = upload_dataset_template(yaml_file)
        template_ids += [template_id]

    return template_ids


@print_function_name_decorator
def upload_dataset_file(dataset_id, file_path):
    api_client = get_swagger_client()
    api_instance = swagger_client.DatasetServiceApi(api_client=api_client)

    try:
        response = api_instance.upload_dataset_file(id=dataset_id, uploadfile=file_path)
        print(f"Upload file '{file_path}' to dataset with ID '{dataset_id}'")

    except ApiException as e:
        print("Exception when calling DatasetServiceApi -> upload_dataset_file: %s\n" % e, file=stderr)
        raise e


@print_function_name_decorator
def download_dataset_tgz(dataset_id) -> str:
    api_client = get_swagger_client()
    api_instance = swagger_client.DatasetServiceApi(api_client=api_client)

    try:
        response: HTTPResponse = \
            api_instance.download_dataset_files(dataset_id,
                                                include_generated_code=True,
                                                _preload_content=False)

        attachment_header = response.info().get("Content-Disposition",
                                                f"attachment; filename={dataset_id}.tgz")

        download_filename = re.sub("attachment; filename=", "", attachment_header)

        download_dir = os.path.join(tempfile.gettempdir(), "download", "datasets")
        os.makedirs(download_dir, exist_ok=True)
        tarfile_path = os.path.join(download_dir, download_filename)

        with open(tarfile_path, 'wb') as f:
            f.write(response.read())

        print(tarfile_path)

        return tarfile_path

    except ApiException as e:
        print("Exception when calling DatasetServiceApi -> download_dataset_files: %s\n" % e, file=stderr)

    return "Download failed?"


@print_function_name_decorator
def verify_dataset_download(dataset_id: str) -> bool:
    api_client = get_swagger_client()
    api_instance = swagger_client.DatasetServiceApi(api_client=api_client)

    try:
        response: HTTPResponse = \
            api_instance.download_dataset_files(dataset_id,
                                                include_generated_code=True,
                                                _preload_content=False)
        tgz_file = BytesIO(response.read())
        tar = tarfile.open(fileobj=tgz_file)

        file_contents = {m.name.split(".")[-1]: tar.extractfile(m).read().decode("utf-8")
                         for m in tar.getmembers()}

        template_response: ApiGetTemplateResponse = api_instance.get_dataset_template(dataset_id)
        template_text_from_api = template_response.template

        assert template_text_from_api == file_contents.get("yaml", file_contents.get("yml"))

        # TODO: verify generated code
        # generate_code_response: ApiGenerateCodeResponse = api_instance.generate_dataset_code(dataset_id)
        # run_script_from_api = generate_code_response.script
        #
        # regex = re.compile(r"name='[^']*'")  # controller adds random chars to name, replace those
        #
        # assert regex.sub("name='...'", run_script_from_api) == \
        #        regex.sub("name='...'", file_contents.get("py"))

        print("downloaded files match")

        return True

    except ApiException as e:
        print("Exception when calling DatasetServiceApi -> download_dataset_files: %s\n" % e, file=stderr)

    return False


@print_function_name_decorator
def approve_datasets_for_publishing(dataset_ids: [str]):
    api_client = get_swagger_client()
    api_instance = swagger_client.DatasetServiceApi(api_client=api_client)

    try:
        api_response = api_instance.approve_datasets_for_publishing(dataset_ids)

    except ApiException as e:
        print("Exception when calling DatasetServiceApi -> approve_datasets_for_publishing: %s\n" % e, file=stderr)

    return None


@print_function_name_decorator
def set_featured_datasets(dataset_ids: [str]):
    api_client = get_swagger_client()
    api_instance = swagger_client.DatasetServiceApi(api_client=api_client)

    try:
        api_response = api_instance.set_featured_datasets(dataset_ids)

    except ApiException as e:
        print("Exception when calling DatasetServiceApi -> set_featured_datasets: %s\n" % e, file=stderr)

    return None


@print_function_name_decorator
def get_dataset(dataset_id: str) -> ApiDataset:
    api_client = get_swagger_client()
    api_instance = swagger_client.DatasetServiceApi(api_client=api_client)

    try:
        dataset_meta: ApiDataset = api_instance.get_dataset(dataset_id)
        pprint(dataset_meta, indent=2)
        return dataset_meta

    except ApiException as e:
        print("Exception when calling DatasetServiceApi -> get_dataset: %s\n" % e, file=stderr)

    return None


@print_function_name_decorator
def delete_dataset(dataset_id: str):
    api_client = get_swagger_client()
    api_instance = swagger_client.DatasetServiceApi(api_client=api_client)

    try:
        api_instance.delete_dataset(dataset_id)
    except ApiException as e:
        print("Exception when calling DatasetServiceApi -> delete_dataset: %s\n" % e, file=stderr)


@print_function_name_decorator
def get_template(template_id: str) -> str:
    api_client = get_swagger_client()
    api_instance = swagger_client.DatasetServiceApi(api_client=api_client)

    try:
        template_response: ApiGetTemplateResponse = api_instance.get_dataset_template(template_id)
        print(template_response.template)

        # yaml_dict = yaml.load(template_response.template, Loader=yaml.FullLoader)
        # dataset_name = yaml_dict.get("name") or f"template_{template_id}"
        # template_file = os.path.join("files", dataset_name) + ".yaml"

        # with open(template_file, "w") as f:
        #     f.write(template_response.template)

        return template_response.template

    except ApiException as e:
        print("Exception when calling DatasetServiceApi -> get_dataset_template: %s\n" % e, file=stderr)

    return None


@print_function_name_decorator
def generate_code(dataset_id: str) -> str:
    api_client = get_swagger_client()
    api_instance = swagger_client.DatasetServiceApi(api_client=api_client)

    try:
        generate_code_response: ApiGenerateCodeResponse = api_instance.generate_dataset_code(dataset_id)
        print(generate_code_response.script)

        return generate_code_response.script

    except ApiException as e:
        print("Exception while calling DatasetServiceApi -> generate_code: %s\n" % e, file=stderr)

    return None


@print_function_name_decorator
def run_code(dataset_id: str, parameters: dict = {}, run_name: str = None) -> str:
    api_client = get_swagger_client()
    api_instance = swagger_client.DatasetServiceApi(api_client=api_client)

    try:
        param_array = [{"name": key, "value": value} for key, value in parameters.items()]
        run_code_response: ApiRunCodeResponse = api_instance.run_dataset(dataset_id,
                                                                         run_name=run_name,
                                                                         parameters=param_array)
        print(run_code_response.run_url)

        return run_code_response.run_url

    except ApiException as e:
        print("Exception while calling DatasetServiceApi -> run_code: %s\n" % e, file=stderr)

    return None


@print_function_name_decorator
def list_datasets(filter_dict: dict = {}, sort_by: str = None) -> [ApiDataset]:
    api_client = get_swagger_client()
    api_instance = swagger_client.DatasetServiceApi(api_client=api_client)

    try:
        filter_str = json.dumps(filter_dict) if filter_dict else None

        api_response: ApiListDatasetsResponse = api_instance.list_datasets(filter=filter_str, sort_by=sort_by)

        for c in api_response.datasets:
            print("%s  %s  %s" % (c.id, c.created_at.strftime("%Y-%m-%d %H:%M:%S"), c.name))

        return api_response.datasets

    except ApiException as e:
        print("Exception when calling DatasetServiceApi -> list_datasets: %s\n" % e, file=stderr)

    return []


def main():
    # delete existing datasets
    delete_dataset(dataset_id="*")

    # upload all templates
    dataset_ids: [str] = upload_dataset_templates()

    # list all datasets
    datasets = list_datasets()
    dataset_ids: [str] = [dataset.id for dataset in datasets]

    # set featured datasets
    set_featured_datasets(dataset_ids)

    # approve datasets to be published
    approve_datasets_for_publishing(dataset_ids)

    # randomly selected a dataset
    i = random.randint(0, len(dataset_ids) - 1)
    dataset_id = dataset_ids[i]

    # show one randomly selected dataset
    get_dataset(dataset_id)
    get_template(dataset_id)

    # generate sample pipeline code for dataset
    generate_code(dataset_id)

    # run sample pipeline
    run_code(dataset_id, parameters={"namespace": "kubeflow"})

    # TODO: verify uploaded file(s) match downloaded file(s) (that's different from comparing template with download)
    tgz_file = download_dataset_tgz(dataset_id)
    verify_dataset_download(dataset_id)
    upload_dataset_file(dataset_id, tgz_file)

    # TODO: run DataSet in a Kubeflow Pipeline after generating a training DSL?

    # # delete one dataset
    # delete_dataset(dataset_id)

    # # TODO: update a dataset
    # dataset = list_datasets(filter_dict={"name": "Fashion MNIST"})[0]
    # update_dataset_template(dataset.id, "temp/files/fashion-mnist.yaml")


if __name__ == '__main__':
    pprint(yaml_files)
    main()
