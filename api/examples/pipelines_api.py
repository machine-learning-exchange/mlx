# Copyright 2021 IBM Corporation
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
import typing
import yaml

from io import BytesIO
from os import environ as env
from pprint import pprint
from swagger_client.api_client import ApiClient, Configuration
from swagger_client.models import ApiPipeline, ApiGetTemplateResponse, ApiListPipelinesResponse, \
    ApiGenerateCodeResponse, ApiRunCodeResponse, ApiPipelineExtended, ApiPipelineCustom, ApiPipelineCustomRunPayload, \
    ApiPipelineTask, ApiComponent, ApiNotebook, ApiPipelineTaskArguments, ApiPipelineDAG, ApiPipelineInputs, \
    ApiParameter
from swagger_client.rest import ApiException
from sys import stderr
from types import SimpleNamespace as custom_obj
from urllib3.response import HTTPResponse


host = '127.0.0.1'
port = '8080'
# host = env.get("MLX_API_SERVICE_HOST")
# port = env.get("MLX_API_SERVICE_PORT")

api_base_path = 'apis/v1alpha1'

# yaml_files = glob.glob("./../../pipelines/pipeline-samples/*/*.yaml")
# yaml_files = glob.glob("./../../../kfp-tekton/samples/*/*.yaml")
yaml_files = glob.glob("./../../../kfp-tekton/sdk/python/tests/compiler/testdata/*.yaml")[:10]
# yaml_files = sorted(glob.glob("./../../../katalog/pipeline-samples/*.yaml", recursive=True))


def get_swagger_client():

    config = Configuration()
    config.host = f'http://{host}:{port}/{api_base_path}'
    api_client = ApiClient(configuration=config)

    return api_client


def print_function_name_decorator(func):

    def wrapper(*args, **kwargs):
        print()
        print(f"---[ {func.__name__}{str(args)[:50]}{str(kwargs)[0:50]} ]---")
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


def upload_pipeline_template(uploadfile_name, name: str = None, description: str = None, annotations: str = "") -> str:

    api_client = get_swagger_client()
    api_instance = swagger_client.PipelineServiceApi(api_client=api_client)

    try:
        pipeline: ApiPipeline = api_instance.upload_pipeline(uploadfile=uploadfile_name,
                                                             name=name,
                                                             description=description,
                                                             annotations=annotations)
        print(f"Uploaded '{pipeline.name}': {pipeline.id}")
        return pipeline.id

    except ApiException as e:
        print("Exception when calling PipelineServiceApi -> upload_pipeline: %s\n" % e, file=stderr)
        raise e

    return None


@print_function_name_decorator
def upload_pipeline_templates() -> [str]:

    template_ids = []

    for yaml_file in yaml_files:
        pipeline_name = "test_" + os.path.basename(yaml_file).replace(".yaml", "")
        # tarfile_name = create_tar_file(yaml_file)
        # template_id = upload_pipeline_template(tarfile_name, name=pipeline_name)
        template_id = upload_pipeline_template(yaml_file, name=pipeline_name)
        template_ids += [template_id]

    return template_ids


@print_function_name_decorator
def upload_pipeline_file(pipeline_id, file_path):

    api_client = get_swagger_client()
    api_instance = swagger_client.PipelineServiceApi(api_client=api_client)

    try:
        response = api_instance.upload_pipeline_file(id=pipeline_id, uploadfile=file_path)
        print(f"Upload file '{file_path}' to pipeline with ID '{pipeline_id}'")

    except ApiException as e:
        print("Exception when calling PipelineServiceApi -> upload_pipeline_file: %s\n" % e, file=stderr)
        raise e


@print_function_name_decorator
def download_pipeline_tgz(pipeline_id) -> str:

    api_client = get_swagger_client()
    api_instance = swagger_client.PipelineServiceApi(api_client=api_client)

    try:
        response: HTTPResponse = \
            api_instance.download_pipeline_files(pipeline_id, _preload_content=False)

        attachment_header = response.info().get("Content-Disposition",
                                                f"attachment; filename={pipeline_id}.tgz")

        download_filename = re.sub("attachment; filename=", "", attachment_header)

        download_dir = os.path.join(tempfile.gettempdir(), "download", "pipelines")
        os.makedirs(download_dir, exist_ok=True)
        tarfile_path = os.path.join(download_dir, download_filename)

        with open(tarfile_path, 'wb') as f:
            f.write(response.read())

        print(tarfile_path)

        return tarfile_path

    except ApiException as e:
        print("Exception when calling PipelineServiceApi -> download_pipeline_files: %s\n" % e, file=stderr)

    return "Download failed?"


@print_function_name_decorator
def verify_pipeline_download(pipeline_id: str) -> bool:

    api_client = get_swagger_client()
    api_instance = swagger_client.PipelineServiceApi(api_client=api_client)

    try:
        response: HTTPResponse = api_instance.download_pipeline_files(pipeline_id, _preload_content=False)

        tgz_file = BytesIO(response.read())
        with tarfile.open(fileobj=tgz_file) as tar:
            file_contents = {m.name: tar.extractfile(m).read().decode("utf-8")
                             for m in tar.getmembers()}

        template_response: ApiGetTemplateResponse = api_instance.get_template(pipeline_id)
        template_text_from_api = template_response.template

        assert template_text_from_api == file_contents.get("pipeline.yaml")

        print("downloaded files match")

        return True

    except ApiException as e:
        print("Exception when calling PipelineServiceApi -> download_pipeline_files: %s\n" % e, file=stderr)

    return False


@print_function_name_decorator
def approve_pipelines_for_publishing(pipeline_ids: [str]):

    api_client = get_swagger_client()
    api_instance = swagger_client.PipelineServiceApi(api_client=api_client)

    try:
        api_response = api_instance.approve_pipelines_for_publishing(pipeline_ids)

    except ApiException as e:
        print("Exception when calling PipelineServiceApi -> approve_pipelines_for_publishing: %s\n" % e, file=stderr)

    return None


@print_function_name_decorator
def set_featured_pipelines(pipeline_ids: [str]):

    api_client = get_swagger_client()
    api_instance = swagger_client.PipelineServiceApi(api_client=api_client)

    try:
        api_response = api_instance.set_featured_pipelines(pipeline_ids)

    except ApiException as e:
        print("Exception when calling PipelineServiceApi -> set_featured_pipelines: %s\n" % e, file=stderr)

    return None


@print_function_name_decorator
def get_pipeline(pipeline_id: str) -> ApiPipelineExtended:

    api_client = get_swagger_client()
    api_instance = swagger_client.PipelineServiceApi(api_client=api_client)

    try:
        pipeline_meta: ApiPipelineExtended = api_instance.get_pipeline(pipeline_id)
        pprint(pipeline_meta, indent=2)
        return pipeline_meta

    except ApiException as e:
        print("Exception when calling PipelineServiceApi -> get_pipeline: %s\n" % e, file=stderr)

    return None


@print_function_name_decorator
def delete_pipeline(pipeline_id: str):

    api_client = get_swagger_client()
    api_instance = swagger_client.PipelineServiceApi(api_client=api_client)

    try:
        api_instance.delete_pipeline(pipeline_id)
        
    except ApiException as e:
        print("Exception when calling PipelineServiceApi -> delete_pipeline: %s\n" % e, file=stderr)


@print_function_name_decorator
def get_template(template_id: str) -> str:

    api_client = get_swagger_client()
    api_instance = swagger_client.PipelineServiceApi(api_client=api_client)

    try:
        template_response: ApiGetTemplateResponse = api_instance.get_template(template_id)
        print(template_response.template)

        # yaml_dict = yaml.load(template_response.template, Loader=yaml.FullLoader)
        # pipeline_name = yaml_dict.get("name") or f"template_{template_id}"
        # template_file = os.path.join("files", pipeline_name) + ".yaml"

        # with open(template_file, "w") as f:
        #     f.write(template_response.template)

        return template_response.template

    except ApiException as e:
        print("Exception when calling PipelineServiceApi -> get_pipeline_template: %s\n" % e, file=stderr)

    return None


@print_function_name_decorator
def run_pipeline(pipeline_id: str, parameters: dict = None, run_name: str = None) -> str:

    api_client = get_swagger_client()
    api_instance = swagger_client.PipelineServiceApi(api_client=api_client)

    try:
        run_code_response: ApiRunCodeResponse = api_instance.run_pipeline(pipeline_id, parameters=parameters,
                                                                          run_name=run_name)
        print(run_code_response.run_url)
        return run_code_response.run_url

    except ApiException as e:
        print("Exception while calling PipelineServiceApi -> run_pipeline: %s\n" % e, file=stderr)

    return None


@print_function_name_decorator
def generate_custom_pipeline(sequential_only=False) -> ApiPipelineCustom:

    api_client = get_swagger_client()
    notebooks_api_instance = swagger_client.NotebookServiceApi(api_client=api_client)
    components_api_instance = swagger_client.ComponentServiceApi(api_client=api_client)

    try:
        components: typing.List[ApiComponent] = random.sample(
            list(filter(lambda n: "StudyJob" not in n.name,
                        components_api_instance.list_components().components)), 3)

        # components = []

        notebooks: typing.List[ApiNotebook] = random.sample(
            notebooks_api_instance.list_notebooks().notebooks, 5)

        tasks: typing.List[ApiPipelineTask] = []

        for c in components:
            tasks.append(
                ApiPipelineTask(name=f"component task {c.name}",
                                artifact_type="component",
                                artifact_id=c.id,
                                arguments=ApiPipelineTaskArguments(parameters=c.parameters),
                                dependencies=[]))

        for n in notebooks:
            tasks.append(
                ApiPipelineTask(name=f"notebook task {n.name}",
                                artifact_type="notebook",
                                artifact_id=n.id,
                                arguments=ApiPipelineTaskArguments(parameters=n.parameters),
                                dependencies=[]))

        if sequential_only:
            for i in range(len(tasks)-1):
                tasks[i+1].dependencies = [tasks[i].name]
        else:
            for i in range(len(tasks)):
                num_deps = random.randint(0, i)
                deps_idx = {random.randint(0, i) for n in range(0, num_deps)}
                tasks[i].dependencies = [tasks[i].name for i in sorted(deps_idx)]

        pipeline_params = []

        for t in tasks:
            task_name_prefix = re.sub(r"\W+", "_", t.name, flags=re.ASCII).lower()

            for p in t.arguments.parameters:
                if not (p.value or p.default):
                    param_name = re.sub(r"\W+", "_", p.name, flags=re.ASCII).lower()
                    pipeline_param_name = f"{task_name_prefix}_{param_name}"
                    p.value = "{{inputs.parameters." + pipeline_param_name + "}}"
                    pipeline_params.append(ApiParameter(name=pipeline_param_name, value="some value"))

        api_pipeline_custom = ApiPipelineCustom(
            name="My custom pipeline",
            description="A randomly generated pipeline from notebooks and components",
            dag=ApiPipelineDAG(tasks=tasks),
            inputs=ApiPipelineInputs(parameters=pipeline_params))

        return api_pipeline_custom

    except ApiException as e:
        print(f"Exception while generating custom pipeline DAG with parameters: \n{str(e)}", file=stderr)


@print_function_name_decorator
def run_custom_pipeline(pipeline_template: dict, parameters: list = None, run_name: str = None) -> str:

    api_client = get_swagger_client()
    api_instance = swagger_client.PipelineServiceApi(api_client=api_client)

    try:
        # TODO: cleanup pipeline parameter, we should not support KFP Argo YAML
        if pipeline_template.get("spec", {}).get("templates"):
            # pipeline_dag = [t for t in pipeline_template["spec"]["templates"] if "dag" in t][0]
            pipeline_dag = list(filter(lambda t: "dag" in t, pipeline_template["spec"]["templates"]))[0]
        elif "dag" in pipeline_template:
            pipeline_dag = pipeline_template

        # custom_pipeline = ApiPipelineCustom.from_dict(pipeline_dag)
        mock_response = custom_obj(data=json.dumps(pipeline_dag))
        custom_pipeline = api_client.deserialize(response=mock_response, response_type=ApiPipelineCustom)
        run_custom_pipeline_payload = ApiPipelineCustomRunPayload(custom_pipeline=custom_pipeline,
                                                                  run_parameters=parameters)
        run_code_response: ApiRunCodeResponse = \
            api_instance.run_custom_pipeline(run_custom_pipeline_payload=run_custom_pipeline_payload,
                                             run_name=run_name)
        print(run_code_response.run_url)
        return run_code_response.run_url

    except ApiException as e:
        print("Exception while calling PipelineServiceApi -> run_pipeline: %s\n" % e, file=stderr)

    return None


@print_function_name_decorator
def list_pipelines(filter_dict: dict = {}, sort_by: str = None) -> [ApiPipeline]:

    api_client = get_swagger_client()
    api_instance = swagger_client.PipelineServiceApi(api_client=api_client)

    try:
        filter_str = json.dumps(filter_dict) if filter_dict else None

        api_response: ApiListPipelinesResponse = api_instance.list_pipelines(filter=filter_str, sort_by=sort_by)

        for c in api_response.pipelines:
            print("%s  %s  %s" % (c.id, c.created_at.strftime("%Y-%m-%d %H:%M:%S"), c.name))

        return api_response.pipelines

    except ApiException as e:
        print("Exception when calling PipelineServiceApi -> list_pipelines: %s\n" % e, file=stderr)

    return []


def main():

    # delete existing pipelines, actually, only pipeline_extensions table and pipelines_extended view table
    # delete_pipeline(pipeline_id="*")

    # delete "test_" pipelines
    test_pipelines = list_pipelines(filter_dict={"name": "test_%"})
    for pipeline in test_pipelines:
        delete_pipeline(pipeline.id)

    # upload all templates
    pipeline_ids: [str] = upload_pipeline_templates()

    # list all pipelines
    pipelines = list_pipelines()
    pipeline_ids: [str] = [pipeline.id for pipeline in pipelines]

    # download a pipeline
    tarfile_name = download_pipeline_tgz(pipeline_ids[0])

    # upload a new pipeline with description and annotations
    name = "New pipeline"
    description = "Some description"
    annotations_dict = {"platform": "Kubeflow", "license": "opensource"}
    annotations_str = json.dumps(annotations_dict)
    pipeline_id = upload_pipeline_template(tarfile_name, name, description, annotations_str)
    p = get_pipeline(pipeline_id)
    assert p.description == description and p.annotations == annotations_dict

    # delete the pipeline we just uploaded
    delete_pipeline(pipeline_id)

    # approve pipelines to be published
    approve_pipelines_for_publishing(pipeline_ids[:7])

    # set featured pipelines
    set_featured_pipelines(pipeline_ids[:4])

    # randomly selected a pipeline
    i = random.randint(0, len(pipeline_ids)-1)
    pipeline_id = pipeline_ids[i]

    # show one randomly selected pipeline
    get_pipeline(pipeline_id)
    get_template(pipeline_id)

    verify_pipeline_download(pipeline_id)

    pipelines = list_pipelines(filter_dict={"name": "[Sample] Basic - Parallel execution"}) or \
                list_pipelines(filter_dict={"name": "[Sample] Basic - Parallel Join"}) or \
                list_pipelines(filter_dict={"name": "[Tutorial] DSL - Control structures"}) or \
                list_pipelines(filter_dict={"name": "test_parallel_join"})
    pipeline = pipelines[0]
    arguments = {
        "url1": "gs://ml-pipeline-playground/shakespeare1.txt",
        "url2": "gs://ml-pipeline-playground/shakespeare2.txt"
    }
    run_pipeline(pipeline.id, arguments)

    # TODO: reactivate generating custom pipeline
    # cust_pipeline = generate_custom_pipeline(sequential_only=True)
    # # print(json.dumps(cust_pipeline.to_dict(), indent=2, sort_keys=False, ensure_ascii=True))
    # run_custom_pipeline(cust_pipeline.to_dict(), {"run_arg1": "run_arg1_value"})

    # delete "test_" pipelines
    test_pipelines = list_pipelines(filter_dict={"name": "test_%"})
    for pipeline in test_pipelines:
        delete_pipeline(pipeline.id)


if __name__ == '__main__':
    pprint(yaml_files)
    main()
