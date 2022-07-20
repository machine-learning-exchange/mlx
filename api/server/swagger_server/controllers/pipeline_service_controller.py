# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0

import connexion

from swagger_server.models.api_get_template_response import ApiGetTemplateResponse  # noqa: E501
from swagger_server.models.api_list_pipelines_response import ApiListPipelinesResponse  # noqa: E501
from swagger_server.models.api_pipeline import ApiPipeline  # noqa: E501
from swagger_server.models.api_pipeline_custom_run_payload import ApiPipelineCustomRunPayload  # noqa: E501
from swagger_server.models.api_pipeline_extended import ApiPipelineExtended  # noqa: E501
from swagger_server.models.api_run_code_response import ApiRunCodeResponse  # noqa: E501
from swagger_server.models.api_status import ApiStatus  # noqa: E501
from swagger_server.models.dictionary import Dictionary  # noqa: E501
from swagger_server import util


def approve_pipelines_for_publishing(pipeline_ids):  # noqa: E501
    """approve_pipelines_for_publishing

     # noqa: E501

    :param pipeline_ids: Array of pipeline IDs to be approved for publishing.
    :type pipeline_ids: List[]

    :rtype: None
    """
    return util.invoke_controller_impl()


def create_pipeline(body):  # noqa: E501
    """create_pipeline

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: ApiPipeline
    """
    if connexion.request.is_json:
        body = ApiPipeline.from_dict(connexion.request.get_json())  # noqa: E501
    return util.invoke_controller_impl()


def delete_pipeline(id):  # noqa: E501
    """delete_pipeline

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: None
    """
    return util.invoke_controller_impl()


def download_pipeline_files(id):  # noqa: E501
    """Returns the pipeline YAML compressed into a .tgz (.tar.gz) file.

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: file | binary
    """
    return util.invoke_controller_impl()


def get_pipeline(id):  # noqa: E501
    """get_pipeline

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: ApiPipelineExtended
    """
    return util.invoke_controller_impl()


def get_template(id):  # noqa: E501
    """get_template

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: ApiGetTemplateResponse
    """
    return util.invoke_controller_impl()


def list_pipelines(page_token=None, page_size=None, sort_by=None, filter=None):  # noqa: E501
    """list_pipelines

     # noqa: E501

    :param page_token: 
    :type page_token: str
    :param page_size: 
    :type page_size: int
    :param sort_by: Can be format of \&quot;field_name\&quot;, \&quot;field_name asc\&quot; or \&quot;field_name desc\&quot; Ascending by default.
    :type sort_by: str
    :param filter: A string-serialized JSON dictionary with key-value pairs that correspond to the Pipeline&#39;s attribute names and their respective values to be filtered for.
    :type filter: str

    :rtype: ApiListPipelinesResponse
    """
    return util.invoke_controller_impl()


def run_custom_pipeline(run_custom_pipeline_payload, run_name=None):  # noqa: E501
    """run_custom_pipeline

    Run a complex pipeline defined by a directed acyclic graph (DAG) # noqa: E501

    :param run_custom_pipeline_payload: A custom pipeline defined by a directed acyclic graph (DAG) and input parameters
    :type run_custom_pipeline_payload: dict | bytes
    :param run_name: Name to identify the run on the Kubeflow Pipelines UI
    :type run_name: str

    :rtype: ApiRunCodeResponse
    """
    if connexion.request.is_json:
        run_custom_pipeline_payload = ApiPipelineCustomRunPayload.from_dict(connexion.request.get_json())  # noqa: E501
    return util.invoke_controller_impl()


def run_pipeline(id, run_name=None, parameters=None):  # noqa: E501
    """run_pipeline

     # noqa: E501

    :param id: 
    :type id: str
    :param run_name: name to identify the run on the Kubeflow Pipelines UI, defaults to pipeline name
    :type run_name: str
    :param parameters: optional run parameters, may be required based on pipeline definition
    :type parameters: dict | bytes

    :rtype: ApiRunCodeResponse
    """
    if connexion.request.is_json:
        parameters = Dictionary.from_dict(connexion.request.get_json())  # noqa: E501
    return util.invoke_controller_impl()


def set_featured_pipelines(pipeline_ids):  # noqa: E501
    """set_featured_pipelines

     # noqa: E501

    :param pipeline_ids: Array of pipeline IDs to be featured.
    :type pipeline_ids: List[]

    :rtype: None
    """
    return util.invoke_controller_impl()


def upload_pipeline(uploadfile, name=None, description=None, annotations=None):  # noqa: E501
    """upload_pipeline

     # noqa: E501

    :param uploadfile: The pipeline YAML file to upload. Can be a GZip-compressed TAR file (.tgz, .tar.gz) or a YAML file (.yaml, .yml). Maximum size is 32MB.
    :type uploadfile: werkzeug.datastructures.FileStorage
    :param name: A name for this pipeline, optional
    :type name: str
    :param description: A description for this pipeline, optional
    :type description: str
    :param annotations: A string representation of a JSON dictionary of annotations describing this pipeline, optional. Example: {\&quot;platform\&quot;: \&quot;Kubeflow\&quot;, \&quot;license\&quot;: \&quot;Opensource\&quot;}
    :type annotations: str

    :rtype: ApiPipelineExtended
    """
    return util.invoke_controller_impl()


def upload_pipeline_from_url(url, name=None, access_token=None):  # noqa: E501
    """upload_pipeline_from_url

     # noqa: E501

    :param url: URL pointing to the pipeline YAML file.
    :type url: str
    :param name: Optional, the name of the pipeline to be created overriding the name in the YAML file.
    :type name: str
    :param access_token: Optional, the Bearer token to access the &#39;url&#39;.
    :type access_token: str

    :rtype: ApiPipeline
    """
    return util.invoke_controller_impl()
