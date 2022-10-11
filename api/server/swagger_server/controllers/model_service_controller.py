# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0

import connexion

from swagger_server.models.api_generate_model_code_response import ApiGenerateModelCodeResponse  # noqa: E501
from swagger_server.models.api_get_template_response import ApiGetTemplateResponse  # noqa: E501
from swagger_server.models.api_list_models_response import ApiListModelsResponse  # noqa: E501
from swagger_server.models.api_model import ApiModel  # noqa: E501
from swagger_server.models.api_run_code_response import ApiRunCodeResponse  # noqa: E501
from swagger_server.models.api_status import ApiStatus  # noqa: E501
from swagger_server.models.dictionary import Dictionary  # noqa: E501
from swagger_server import util


def approve_models_for_publishing(model_ids):  # noqa: E501
    """approve_models_for_publishing

     # noqa: E501

    :param model_ids: Array of model IDs to be approved for publishing.
    :type model_ids: List[]

    :rtype: None
    """
    return util.invoke_controller_impl()


def create_model(body):  # noqa: E501
    """create_model

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: ApiModel
    """
    if connexion.request.is_json:
        body = ApiModel.from_dict(connexion.request.get_json())  # noqa: E501
    return util.invoke_controller_impl()


def delete_model(id):  # noqa: E501
    """delete_model

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: None
    """
    return util.invoke_controller_impl()


def download_model_files(id, include_generated_code=None):  # noqa: E501
    """Returns the model artifacts compressed into a .tgz (.tar.gz) file.

     # noqa: E501

    :param id: 
    :type id: str
    :param include_generated_code: Include generated run scripts in download
    :type include_generated_code: bool

    :rtype: file | binary
    """
    return util.invoke_controller_impl()


def generate_model_code(id):  # noqa: E501
    """generate_model_code

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: ApiGenerateModelCodeResponse
    """
    return util.invoke_controller_impl()


def get_model(id):  # noqa: E501
    """get_model

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: ApiModel
    """
    return util.invoke_controller_impl()


def get_model_template(id):  # noqa: E501
    """get_model_template

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: ApiGetTemplateResponse
    """
    return util.invoke_controller_impl()


def list_models(page_token=None, page_size=None, sort_by=None, filter=None):  # noqa: E501
    """list_models

     # noqa: E501

    :param page_token: 
    :type page_token: str
    :param page_size: 
    :type page_size: int
    :param sort_by: Can be format of \&quot;field_name\&quot;, \&quot;field_name asc\&quot; or \&quot;field_name desc\&quot; Ascending by default.
    :type sort_by: str
    :param filter: A string-serialized JSON dictionary with key-value pairs that correspond to the Model&#39;s attribute names and their respective values to be filtered for.
    :type filter: str

    :rtype: ApiListModelsResponse
    """
    return util.invoke_controller_impl()


def run_model(id, pipeline_stage, execution_platform, run_name=None, parameters=None):  # noqa: E501
    """run_model

     # noqa: E501

    :param id: 
    :type id: str
    :param pipeline_stage: pipeline stage, either 'train' or 'serve'
    :type pipeline_stage: str
    :param execution_platform: execution platform, i.e. 'kubernetes', 'knative'
    :type execution_platform: str
    :param run_name: name to identify the run on the Kubeflow Pipelines UI, defaults to model identifier
    :type run_name: str
    :param parameters: optional run parameters, must include 'github_token' and 'github_url' if credentials are required
    :type parameters: dict

    :rtype: ApiRunCodeResponse
    """
    if connexion.request.is_json:
        parameters = Dictionary.from_dict(connexion.request.get_json())  # noqa: E501
    return util.invoke_controller_impl()


def set_featured_models(model_ids):  # noqa: E501
    """set_featured_models

     # noqa: E501

    :param model_ids: Array of model IDs to be featured.
    :type model_ids: List[]

    :rtype: None
    """
    return util.invoke_controller_impl()


def upload_model(uploadfile, name=None):  # noqa: E501
    """upload_model

     # noqa: E501

    :param uploadfile: The model YAML file to upload. Can be a GZip-compressed TAR file (.tgz, .tar.gz) or a YAML file (.yaml, .yml). Maximum size is 32MB.
    :type uploadfile: werkzeug.datastructures.FileStorage
    :param name: 
    :type name: str

    :rtype: ApiModel
    """
    return util.invoke_controller_impl()


def upload_model_file(id, uploadfile):  # noqa: E501
    """upload_model_file

     # noqa: E501

    :param id: The model identifier.
    :type id: str
    :param uploadfile: The file to upload, overwriting existing. Can be a GZip-compressed TAR file (.tgz), a YAML file (.yaml), Python script (.py), or Markdown file (.md)
    :type uploadfile: werkzeug.datastructures.FileStorage

    :rtype: ApiModel
    """
    return util.invoke_controller_impl()


def upload_model_from_url(url, name=None, access_token=None):  # noqa: E501
    """upload_model_from_url

     # noqa: E501

    :param url: URL pointing to the model YAML file.
    :type url: str
    :param name: Optional, the name of the model to be created overriding the name in the YAML file.
    :type name: str
    :param access_token: Optional, the Bearer token to access the &#39;url&#39;.
    :type access_token: str

    :rtype: ApiModel
    """
    return util.invoke_controller_impl()
