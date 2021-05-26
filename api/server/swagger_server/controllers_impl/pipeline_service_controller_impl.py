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

import connexion
import json
import os
import tarfile
import typing
import yaml

from datetime import datetime
from collections import Counter
from os import environ as env
from typing import AnyStr

from swagger_server.controllers_impl import download_file_content_from_url
from swagger_server.controllers_impl import get_yaml_file_content_from_uploadfile
from swagger_server.data_access.minio_client import store_file, delete_object, \
    delete_objects, retrieve_file_content, retrieve_file_content_and_url, \
    enable_anonymous_read_access, create_tarfile
from swagger_server.data_access.mysql_client import store_data, generate_id, load_data, \
    delete_data, num_rows, update_multiple
from swagger_server.gateways.kubeflow_pipeline_service import upload_pipeline_to_kfp,\
    delete_kfp_pipeline, run_pipeline_in_experiment, run_custom_pipeline_in_experiment, \
    _host as KFP_HOST
from swagger_server.models.api_get_template_response import ApiGetTemplateResponse  # noqa: E501
from swagger_server.models.api_list_pipelines_response import ApiListPipelinesResponse  # noqa: E501
from swagger_server.models.api_pipeline import ApiPipeline  # noqa: E501
from swagger_server.models import ApiPipelineCustomRunPayload, ApiPipelineTask, ApiPipelineDAG
from swagger_server.models.api_metadata import ApiMetadata
from swagger_server.models.api_parameter import ApiParameter
from swagger_server.models.api_pipeline_extension import ApiPipelineExtension  # noqa: E501
from swagger_server.models.api_pipeline_extended import ApiPipelineExtended  # noqa: E501
from swagger_server.models.api_run_code_response import ApiRunCodeResponse  # noqa: E501
from tempfile import mkstemp


def approve_pipelines_for_publishing(pipeline_ids):  # noqa: E501
    """approve_pipelines_for_publishing

    :param pipeline_ids: Array of pipeline IDs to be approved for publishing.
    :type pipeline_ids: List[str]

    :rtype: None
    """
    pipe_exts: [ApiPipelineExtension] = load_data(ApiPipelineExtension)
    pipe_ext_ids = {p.id for p in pipe_exts}
    missing_pipe_ext_ids = set(pipeline_ids) - pipe_ext_ids

    for id in missing_pipe_ext_ids:
        store_data(ApiPipelineExtension(id=id))

    update_multiple(ApiPipelineExtension, [], "publish_approved", False)

    if pipeline_ids:
        update_multiple(ApiPipelineExtension, pipeline_ids, "publish_approved", True)

    return None, 200


def create_pipeline(body):  # noqa: E501
    """create_pipeline

    :param body: 
    :type body: dict | bytes

    :rtype: ApiPipeline
    """
    if connexion.request.is_json:
        body = ApiPipeline.from_dict(connexion.request.get_json())  # noqa: E501

    return "Not implemented, yet", 501


def delete_pipeline(id):  # noqa: E501
    """delete_pipeline

    :param id: 
    :type id: str

    :rtype: None
    """

    if KFP_HOST == "UNAVAILABLE":
        # TODO delete pipeline_versions first
        delete_data(ApiPipeline, id)
        if id == "*":
            delete_objects(bucket_name="mlpipeline", prefix=f"pipelines/")
        else:
            delete_object(bucket_name="mlpipeline", prefix="pipelines", file_name=f"{id}")
    else:
        # wildcard '*' deletes (and recreates) entire table, not desired for pipelines table, KFP API does not accept "*"
        if id != "*":
            delete_kfp_pipeline(id)

    delete_data(ApiPipelineExtension, id)

    # wildcard '*' deletes (and recreates) entire table, forced schema migration for pipeline_extensions table
    if id == "*":
        delete_data(ApiPipelineExtended, id)

    return None, 200


def download_pipeline_files(id):  # noqa: E501
    """Returns the pipeline YAML compressed into a .tgz (.tar.gz) file.

    :param id:
    :type id: str

    :rtype: file
    """
    tar, bytes_io = create_tarfile(bucket_name="mlpipeline", prefix=f"pipelines/{id}",
                                   file_extensions=[""],
                                   keep_open=False)

    if len(tar.members) == 0:
        return f"Could not find pipeline with id '{id}'", 404

    return bytes_io.getvalue(), 200, {"Content-Disposition": f"attachment; filename={id}.tgz"}


def get_pipeline(id):  # noqa: E501
    """get_pipeline

    :param id:
    :type id: str

    :rtype: ApiPipelineExtended
    """
    api_pipelines: [ApiPipelineExtended] = load_data(ApiPipelineExtended, filter_dict={"id": id})

    if not api_pipelines:
        return "Not found", 404

    api_pipeline = api_pipelines[0]

    return api_pipeline, 200


def get_template(id):  # noqa: E501
    """get_template

    :param id: 
    :type id: str

    :rtype: ApiGetTemplateResponse
    """
    files_w_url = retrieve_file_content_and_url(bucket_name="mlpipeline", prefix=f"pipelines/{id}",
                                                file_extensions=[""])
    if files_w_url:
        template_yaml, url = files_w_url[0]
        template_response = ApiGetTemplateResponse(template=template_yaml, url=url)
        return template_response, 200

    else:
        return f"Pipeline template with id '{id}' does not exist", 404


def list_pipelines(page_token=None, page_size=None, sort_by=None, filter=None):  # noqa: E501
    """list_pipelines

    :param page_token: 
    :type page_token: str
    :param page_size: 
    :type page_size: int
    :param sort_by: Can be format of \&quot;field_name\&quot;, \&quot;field_name asc\&quot; or \&quot;field_name des\&quot; Ascending by default.
    :type sort_by: str
    :param filter: A string-serialized JSON dictionary containing key-value pairs with name of the object property to apply filter on and the value of the respective property.
    :type filter: str

    :rtype: ApiListPipelinesResponse
    """

    if page_size == 0:
        return {}, 200

    # TODO: do not misuse page_token as MySQL result offset
    offset = int(page_token) if page_token and page_token.isdigit() else 0

    filter_dict = json.loads(filter) if filter else None

    api_pipelines: [ApiPipeline] = load_data(ApiPipelineExtended, filter_dict=filter_dict, sort_by=sort_by,
                                             count=page_size, offset=offset)

    next_page_token = offset + page_size if len(api_pipelines) == page_size else None

    total_size = num_rows(ApiPipeline)

    if total_size == next_page_token:
        next_page_token = None

    pipeline_list = ApiListPipelinesResponse(pipelines=api_pipelines, total_size=total_size,
                                             next_page_token=next_page_token)
    return pipeline_list, 200


def run_custom_pipeline(run_custom_pipeline_payload, run_name=None):  # noqa: E501
    """run_custom_pipeline

    Run a complex pipeline defined by a directed acyclic graph (DAG)

    :param run_custom_pipeline_payload: A custom pipeline defined by a directed acyclic graph (DAG) and input parameters
    :type run_custom_pipeline_payload: dict | bytes
    :param run_name: Name to identify the run on the Kubeflow Pipelines UI
    :type run_name: str

    :rtype: ApiRunCodeResponse
    """
    if connexion.request.is_json:
        run_custom_pipeline_payload = ApiPipelineCustomRunPayload.from_dict(connexion.request.get_json())  # noqa: E501

    run_parameters = run_custom_pipeline_payload.run_parameters or {}
    custom_pipeline = run_custom_pipeline_payload.custom_pipeline

    # ensure unique task names
    task_names = [t.name for t in custom_pipeline.dag.tasks]
    duplicate_task_names = [name for name, count in Counter(task_names).items() if count > 1]
    assert not duplicate_task_names, f"duplicate task names: {duplicate_task_names}"

    # validate pipeline dependencies
    pipeline_tasks_by_name: typing.Dict[str, ApiPipelineTask] = {t.name: t for t in custom_pipeline.dag.tasks}
    for t in pipeline_tasks_by_name.values():
        for required_task_name in t.dependencies or []:
            assert required_task_name in pipeline_tasks_by_name, \
                f"missing task '{required_task_name}', as dependency for task '{t.name}'"

    # validate input parameters
    missing_run_parameters = {p.name for p in custom_pipeline.inputs.parameters
                              if p.default is None and p.value is None} - run_parameters.keys()
    assert not missing_run_parameters, f"missing parameters to run pipeline: {missing_run_parameters}"

    # make sure we enable anonymous read access to pipeline task components
    for artifact_type in set([t.artifact_type for t in  pipeline_tasks_by_name.values()]):
        enable_anonymous_read_access(bucket_name="mlpipeline", prefix=f"{artifact_type}s/*")

    try:
        run_id = run_custom_pipeline_in_experiment(custom_pipeline, run_name, run_parameters)
        return ApiRunCodeResponse(run_url=f"/runs/details/{run_id}"), 200

    except Exception as e:
        # TODO: remove traceback?
        import traceback
        print(traceback.format_exc())
        return f"Error while trying to run custom pipeline '{run_name}': {e}", 500


def run_pipeline(id, run_name=None, parameters=None):  # noqa: E501
    """run_pipeline

    :param id:
    :type id: str
    :param run_name: name to identify the run on the Kubeflow Pipelines UI, defaults to pipeline name
    :type run_name: str
    :param parameters: optional run parameters, may be required based on pipeline definition
    :type parameters: dict

    :rtype: ApiRunCodeResponse
    """
    if KFP_HOST == "UNAVAILABLE":
        return f"Kubeflow Pipeline host is 'UNAVAILABLE'", 501

    if not parameters and connexion.request.is_json:
        parameter_dict = dict(connexion.request.get_json())  # noqa: E501
    else:
        parameter_dict = parameters

    api_pipeline, status_code = get_pipeline(id)

    if status_code > 200:
        return f"Pipeline with id '{id}' does not exist", 404

    parameter_errors, status_code = _validate_parameters(api_pipeline, parameter_dict)

    if parameter_errors:
        return parameter_errors, status_code

    try:
        run_id = run_pipeline_in_experiment(api_pipeline, parameter_dict, run_name)
        return ApiRunCodeResponse(run_url=f"/runs/details/{run_id}"), 200

    except Exception as e:
        return f"Error while trying to run pipeline {id}: {e}", 500


def set_featured_pipelines(pipeline_ids):  # noqa: E501
    """set_featured_pipelines

    :param pipeline_ids: Array of pipeline IDs to be featured.
    :type pipeline_ids: List[str]

    :rtype: None
    """
    pipe_exts: [ApiPipelineExtension] = load_data(ApiPipelineExtension)
    pipe_ext_ids = {p.id for p in pipe_exts}
    missing_pipe_ext_ids = set(pipeline_ids) - pipe_ext_ids

    for id in missing_pipe_ext_ids:
        store_data(ApiPipelineExtension(id=id))

    update_multiple(ApiPipelineExtension, [], "featured", False)

    if pipeline_ids:
        update_multiple(ApiPipelineExtension, pipeline_ids, "featured", True)

    return None, 200


def upload_pipeline(uploadfile, name=None, description=None, labels=None, annotations=None):  # noqa: E501
    """upload_pipeline

    :param uploadfile: The pipeline to upload. Maximum size of 32MB is supported.
    :type uploadfile: werkzeug.datastructures.FileStorage
    :param name: A name for this pipeline, optional
    :type name: str
    :param description: A description for this pipeline, optional
    :type description: str
    :param labels: A string representation of a JSON dictionary of labels describing this pipeline, optional.See https://kubernetes.io/docs/concepts/overview/working-with-objects/labels
    :type labels: str
    :param annotations: A string representation of a JSON dictionary of annotations describing this pipeline, optional.See https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations
    :type annotations: str

    :rtype: ApiPipelineExtended
    """
    yaml_file_content = get_yaml_file_content_from_uploadfile(uploadfile)

    return _upload_pipeline_yaml(yaml_file_content, name, description, labels, annotations)


def upload_pipeline_from_url(url, name=None, access_token=None):  # noqa: E501
    """upload_pipeline_from_url

    :param url: URL pointing to the pipeline YAML file.
    :type url: str
    :param name: Optional, the name of the pipeline to be created overriding the name in the YAML file.
    :type name: str
    :param access_token: Optional, the Bearer token to access the &#39;url&#39;.
    :type access_token: str

    :rtype: ApiPipeline
    """
    yaml_file_content = download_file_content_from_url(url, access_token)

    return _upload_pipeline_yaml(yaml_file_content, name)


###############################################################################
#   private helper methods, not swagger-generated
###############################################################################

def _upload_pipeline_yaml(yaml_file_content: AnyStr, name=None, description=None, labels=None, annotations=None):

    (fd, filename) = mkstemp(suffix=".yaml")

    try:
        with os.fdopen(fd, "wb") as f:
            f.write(yaml_file_content)

        if KFP_HOST == "UNAVAILABLE":
            # inside docker-compose we don't have KFP
            api_pipeline: ApiPipeline = _store_pipeline(yaml_file_content, name, description)
        else:
            api_pipeline: ApiPipeline = upload_pipeline_to_kfp(uploadfile=filename, name=name)

        if description:
            update_multiple(ApiPipeline, [api_pipeline.id], "description", description)

        store_data(ApiPipelineExtension(id=api_pipeline.id))

        if annotations:
            if type(annotations) == str:
                annotations = json.loads(annotations)
            update_multiple(ApiPipelineExtension, [api_pipeline.id], "annotations", annotations)

        api_pipeline_extended, _ = get_pipeline(api_pipeline.id)

    finally:
        os.remove(filename)

    return api_pipeline_extended, 201


def _store_pipeline(yaml_file_content: AnyStr, name=None, description=None):

    yaml_dict = yaml.load(yaml_file_content, Loader=yaml.FullLoader)

    template_metadata = yaml_dict.get("metadata") or dict()
    annotations = template_metadata.get("annotations", {})
    pipeline_spec = json.loads(annotations.get("pipelines.kubeflow.org/pipeline_spec", "{}"))

    name = name or template_metadata["name"]
    description = pipeline_spec.get("description", "").strip()
    namespace = pipeline_spec.get("namespace", "").strip()
    pipeline_id = "-".join([generate_id(length=l) for l in [8, 4, 4, 4, 12]])
    created_at = datetime.now()

    parameters = [ApiParameter(name=p.get("name"), description=p.get("description"),
                               default=p.get("default"), value=p.get("value"))
                  for p in yaml_dict["spec"].get("params", {})]

    api_pipeline = ApiPipeline(id=pipeline_id,
                               created_at=created_at,
                               name=name,
                               description=description,
                               parameters=parameters,
                               namespace=namespace)

    uuid = store_data(api_pipeline)

    api_pipeline.id = uuid

    store_file(bucket_name="mlpipeline", prefix=f"pipelines/",
               file_name=f"{pipeline_id}", file_content=yaml_file_content)

    enable_anonymous_read_access(bucket_name="mlpipeline", prefix="pipelines/*")

    return api_pipeline


def _validate_parameters(api_pipeline: ApiPipeline, parameters: dict) -> (str, int):

    acceptable_parameters = [p.name for p in api_pipeline.parameters]
    unexpected_parameters = set(parameters.keys()) - set(acceptable_parameters)

    if unexpected_parameters:
        return f"Unexpected parameter(s): {list(unexpected_parameters)}. " \
               f"Acceptable parameter(s): {acceptable_parameters}", 422

    missing_parameters = [p.name for p in api_pipeline.parameters
                          if not (p.default or p.value) and p.name not in parameters]

    # TODO: figure out a way to determine if a pipeline parameter is required or not.
    #       just testing for default value is not an indicator
    # if missing_parameters:
    #     return f"Missing required parameter(s): {missing_parameters}", 422

    return None, 200
