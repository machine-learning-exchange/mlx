# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import print_function

import json
import os
import random
import re
import requests
import swagger_client  # noqa: F401
import tarfile
import tempfile
import yaml  # noqa: F401

from glob import glob
from io import BytesIO
from os import environ as env  # noqa: F401
from pprint import pprint  # noqa: F401
from swagger_client.api_client import ApiClient, Configuration
from swagger_client.models import (
    ApiNotebook,
    ApiGetTemplateResponse,
    ApiListNotebooksResponse,
    ApiGenerateCodeResponse,
    ApiRunCodeResponse,
)
from swagger_client.rest import ApiException  # noqa: F401
from sys import stderr
from urllib3.response import HTTPResponse  # noqa: F401


host = "127.0.0.1"
port = "8080"
# host = env.get("MLX_API_SERVICE_HOST")
# port = env.get("MLX_API_SERVICE_PORT")

api_base_path = "apis/v1alpha1"

yaml_files = sorted(
    filter(
        lambda f: "template" not in f,
        glob("./../../../katalog/notebook-samples/*.yaml", recursive=True),
    )
)

IBM_GHE_API_TOKEN = env.get("IBM_GHE_API_TOKEN")


def get_swagger_client():

    config = Configuration()
    config.host = f"http://{host}:{port}/{api_base_path}"
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


def upload_notebook_template(uploadfile_name, name=None, ghe_token=None) -> str:

    api_client = get_swagger_client()
    api_instance = swagger_client.NotebookServiceApi(api_client=api_client)

    try:
        if ghe_token:
            notebook: ApiNotebook = api_instance.upload_notebook(
                uploadfile=uploadfile_name, name=name, enterprise_github_token=ghe_token
            )
        else:
            notebook: ApiNotebook = api_instance.upload_notebook(
                uploadfile=uploadfile_name, name=name
            )

        print(f"Uploaded '{notebook.name}': {notebook.id}")
        return notebook.id

    except ApiException as e:
        print(
            "Exception when calling NotebookServiceApi -> upload_notebook: %s\n" % e,
            file=stderr,
        )
        # raise e

    return None


@print_function_name_decorator
def upload_notebook_templates(yaml_files: [str] = yaml_files) -> [str]:

    template_ids = []

    for yaml_file in yaml_files:
        with open(yaml_file, "rb") as f:
            yaml_dict = yaml.load(f, Loader=yaml.SafeLoader)

        if "github.ibm.com" in yaml_dict["implementation"]["github"]["source"]:
            api_token = IBM_GHE_API_TOKEN
        else:
            api_token = None

        # tarfile_name = create_tar_file(yaml_file)
        # template_id = upload_notebook_template(tarfile_name, ghe_token=api_token)
        template_id = upload_notebook_template(yaml_file, ghe_token=api_token)

        template_ids += [template_id]

    return template_ids


@print_function_name_decorator
def upload_notebook_file(notebook_id, file_path):

    api_client = get_swagger_client()
    api_instance = swagger_client.NotebookServiceApi(api_client=api_client)

    try:
        response = api_instance.upload_notebook_file(
            id=notebook_id, uploadfile=file_path
        )
        print(f"Upload file '{file_path}' to notebook with ID '{notebook_id}'")

    except ApiException as e:
        print(
            "Exception when calling NotebookServiceApi -> upload_notebook_file: %s\n"
            % e,
            file=stderr,
        )
        raise e


@print_function_name_decorator
def download_notebook_tgz(
    notebook_id,
    download_dir=os.path.join(tempfile.gettempdir(), "download", "notebooks"),
) -> str:

    api_client = get_swagger_client()
    api_instance = swagger_client.NotebookServiceApi(api_client=api_client)

    try:
        response: HTTPResponse = api_instance.download_notebook_files(
            notebook_id, include_generated_code=True, _preload_content=False
        )

        attachment_header = response.info().get(
            "Content-Disposition", f"attachment; filename={notebook_id}.tgz"
        )

        download_filename = re.sub("attachment; filename=", "", attachment_header)
        os.makedirs(download_dir, exist_ok=True)
        tarfile_path = os.path.join(download_dir, download_filename)

        with open(tarfile_path, "wb") as f:
            f.write(response.read())

        print(tarfile_path)

        return tarfile_path

    except ApiException as e:
        print(
            "Exception when calling NotebookServiceApi -> download_notebook_files: %s\n"
            % e,
            file=stderr,
        )

    return "Download failed?"


@print_function_name_decorator
def verify_notebook_download(notebook_id: str) -> bool:

    api_client = get_swagger_client()
    api_instance = swagger_client.NotebookServiceApi(api_client=api_client)

    try:
        response: HTTPResponse = api_instance.download_notebook_files(
            notebook_id, include_generated_code=True, _preload_content=False
        )
        tgz_file = BytesIO(response.read())
        tar = tarfile.open(fileobj=tgz_file)

        file_contents = {
            m.name.split(".")[-1]: tar.extractfile(m).read().decode("utf-8")
            for m in tar.getmembers()
        }

        template_response: ApiGetTemplateResponse = api_instance.get_notebook_template(
            notebook_id
        )
        template_text_from_api = template_response.template

        assert template_text_from_api == file_contents.get(
            "yaml", file_contents.get("yml")
        )

        generate_code_response: ApiGenerateCodeResponse = (
            api_instance.generate_notebook_code(notebook_id)
        )
        run_script_from_api = generate_code_response.script

        regex = re.compile(
            r"name='[^']*'"
        )  # controller adds random chars to name, replace those

        assert regex.sub("name='...'", run_script_from_api) == regex.sub(
            "name='...'", file_contents.get("py")
        )

        print("downloaded files match")

        return True

    except ApiException as e:
        print(
            "Exception when calling NotebookServiceApi -> download_notebook_files: %s\n"
            % e,
            file=stderr,
        )

    return False


@print_function_name_decorator
def approve_notebooks_for_publishing(notebook_ids: [str]):

    api_client = get_swagger_client()
    api_instance = swagger_client.NotebookServiceApi(api_client=api_client)

    try:
        api_response = api_instance.approve_notebooks_for_publishing(notebook_ids)

    except ApiException as e:
        print(
            "Exception when calling NotebookServiceApi -> approve_notebooks_for_publishing: %s\n"
            % e,
            file=stderr,
        )

    return None


@print_function_name_decorator
def set_featured_notebooks(notebook_ids: [str]):

    api_client = get_swagger_client()
    api_instance = swagger_client.NotebookServiceApi(api_client=api_client)

    try:
        api_response = api_instance.set_featured_notebooks(notebook_ids)

    except ApiException as e:
        print(
            "Exception when calling NotebookServiceApi -> set_featured_notebooks: %s\n"
            % e,
            file=stderr,
        )

    return None


@print_function_name_decorator
def get_notebook(notebook_id: str) -> ApiNotebook:

    api_client = get_swagger_client()
    api_instance = swagger_client.NotebookServiceApi(api_client=api_client)

    try:
        notebook_meta: ApiNotebook = api_instance.get_notebook(notebook_id)
        pprint(notebook_meta, indent=2)
        return notebook_meta

    except ApiException as e:
        print(
            "Exception when calling NotebookServiceApi -> get_notebook: %s\n" % e,
            file=stderr,
        )

    return None


@print_function_name_decorator
def delete_notebook(notebook_id: str):

    api_client = get_swagger_client()
    api_instance = swagger_client.NotebookServiceApi(api_client=api_client)

    try:
        api_instance.delete_notebook(notebook_id)
    except ApiException as e:
        print(
            "Exception when calling NotebookServiceApi -> delete_notebook: %s\n" % e,
            file=stderr,
        )


@print_function_name_decorator
def get_template(template_id: str) -> str:

    api_client = get_swagger_client()
    api_instance = swagger_client.NotebookServiceApi(api_client=api_client)

    try:
        template_response: ApiGetTemplateResponse = api_instance.get_notebook_template(
            template_id
        )
        print(template_response.template)

        # yaml_dict = yaml.load(template_response.template, Loader=yaml.FullLoader)
        # notebook_name = yaml_dict.get("name") or f"template_{template_id}"
        # template_file = os.path.join("files", notebook_name) + ".yaml"

        # with open(template_file, "w") as f:
        #     f.write(template_response.template)

        return template_response.template

    except ApiException as e:
        print(
            "Exception when calling NotebookServiceApi -> get_notebook_template: %s\n"
            % e,
            file=stderr,
        )

    return None


@print_function_name_decorator
def generate_code(notebook_id: str) -> str:

    api_client = get_swagger_client()
    api_instance = swagger_client.NotebookServiceApi(api_client=api_client)

    try:
        generate_code_response: ApiGenerateCodeResponse = (
            api_instance.generate_notebook_code(notebook_id)
        )
        print(generate_code_response.script)

        return generate_code_response.script

    except ApiException as e:
        print(
            "Exception while calling NotebookServiceApi -> generate_code: %s\n" % e,
            file=stderr,
        )

    return None


@print_function_name_decorator
def run_notebook(notebook_id: str, parameters=dict(), run_name: str = None) -> str:

    api_client = get_swagger_client()
    api_instance = swagger_client.NotebookServiceApi(api_client=api_client)

    try:
        run_code_response: ApiRunCodeResponse = api_instance.run_notebook(
            notebook_id, parameters=parameters, run_name=run_name
        )
        print(run_code_response.run_url)
        print(run_code_response.run_output_location)

        return run_code_response.run_url

    except ApiException as e:
        print(
            "Exception while calling NotebookServiceApi -> run_code: %s\n" % e,
            file=stderr,
        )

    return None


@print_function_name_decorator
def list_notebooks(filter_dict: dict = {}, sort_by: str = None) -> [ApiNotebook]:

    api_client = get_swagger_client()
    api_instance = swagger_client.NotebookServiceApi(api_client=api_client)

    try:
        filter_str = json.dumps(filter_dict) if filter_dict else None

        api_response: ApiListNotebooksResponse = api_instance.list_notebooks(
            filter=filter_str, sort_by=sort_by
        )

        for c in api_response.notebooks:
            print(
                "%s  %s  %s"
                % (c.id, c.created_at.strftime("%Y-%m-%d %H:%M:%S"), c.name)
            )

        return api_response.notebooks

    except ApiException as e:
        print(
            "Exception when calling NotebookServiceApi -> list_notebooks: %s\n" % e,
            file=stderr,
        )

    return []


@print_function_name_decorator
def download_notebooks_from_github():

    download_dir = "./temp/download/notebooks"
    os.makedirs(download_dir, exist_ok=True)

    for yaml_file in yaml_files:

        with open(yaml_file, "rb") as f:
            yaml_dict = yaml.load(f, Loader=yaml.SafeLoader)

        url = yaml_dict["implementation"]["github"]["source"]

        download_url = (
            url.replace("/blob", "")
            .replace("github.com", "raw.githubusercontent.com")
            .replace("github.ibm.com", "raw.github.ibm.com")
        )

        if "github.ibm.com" in url:
            headers = {"Authorization": "token %s" % env.get("IBM_GHE_API_TOKEN")}
        else:
            headers = {}

        response = requests.get(download_url, headers=headers, allow_redirects=True)

        if response.status_code == 200:
            with open(os.path.join(download_dir, os.path.basename(url)), "wb") as f:
                f.write(response.content)
        else:
            print(
                "{}: {:20s} --> {}".format(
                    response.status_code, os.path.basename(yaml_file), url
                )
            )


def main():
    # delete existing notebooks
    delete_notebook(notebook_id="*")

    # upload all templates
    notebook_ids: [str] = upload_notebook_templates()

    # list all notebooks
    notebooks = list_notebooks()
    notebook_ids: [str] = [notebook.id for notebook in notebooks]

    # set featured notebooks
    set_featured_notebooks(notebook_ids)

    # approve notebooks to be published
    approve_notebooks_for_publishing(notebook_ids)

    # randomly selected a notebook
    i = random.randint(0, len(notebook_ids) - 1)
    notebook_id = notebook_ids[i]

    # show one randomly selected notebook
    get_notebook(notebook_id)
    get_template(notebook_id)
    download_notebook_tgz(notebook_id)
    verify_notebook_download(notebook_id)
    generate_code(notebook_id)
    run_notebook(notebook_id, run_name=f"test_run_{notebook_id}")

    # notebook = list_notebooks(filter_dict={"name": "AIF360 Bias detection example"})[0]
    # generate_code(notebook.id)
    # run_notebook(notebook.id, run_name="AIF360 bias detection")

    # # delete one notebook
    # delete_notebook(notebook_id)


if __name__ == "__main__":
    pprint(yaml_files)
    main()
    # download_notebooks_from_github()
    # for notebook in list_notebooks():
    #     run_notebook(notebook.id, run_name="My test run for {}".format(notebook.name))
