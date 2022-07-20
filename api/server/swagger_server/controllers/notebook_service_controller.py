# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0

import connexion

from swagger_server.models.api_generate_code_response import ApiGenerateCodeResponse  # noqa: E501
from swagger_server.models.api_get_template_response import ApiGetTemplateResponse  # noqa: E501
from swagger_server.models.api_list_notebooks_response import ApiListNotebooksResponse  # noqa: E501
from swagger_server.models.api_notebook import ApiNotebook  # noqa: E501
from swagger_server.models.api_run_code_response import ApiRunCodeResponse  # noqa: E501
from swagger_server.models.api_status import ApiStatus  # noqa: E501
from swagger_server.models.dictionary import Dictionary  # noqa: E501
from swagger_server import util


def approve_notebooks_for_publishing(notebook_ids):  # noqa: E501
    """approve_notebooks_for_publishing

     # noqa: E501

    :param notebook_ids: Array of notebook IDs to be approved for publishing.
    :type notebook_ids: List[]

    :rtype: None
    """
    return util.invoke_controller_impl()


def create_notebook(body):  # noqa: E501
    """create_notebook

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: ApiNotebook
    """
    if connexion.request.is_json:
        body = ApiNotebook.from_dict(connexion.request.get_json())  # noqa: E501
    return util.invoke_controller_impl()


def delete_notebook(id):  # noqa: E501
    """delete_notebook

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: None
    """
    return util.invoke_controller_impl()


def download_notebook_files(id, include_generated_code=None):  # noqa: E501
    """Returns the notebook artifacts compressed into a .tgz (.tar.gz) file.

     # noqa: E501

    :param id: 
    :type id: str
    :param include_generated_code: Include generated run script in download
    :type include_generated_code: bool

    :rtype: file
    """
    return util.invoke_controller_impl()


def generate_notebook_code(id):  # noqa: E501
    """generate_notebook_code

    Generate sample code to use notebook in a pipeline # noqa: E501

    :param id: 
    :type id: str

    :rtype: ApiGenerateCodeResponse
    """
    return util.invoke_controller_impl()


def get_notebook(id):  # noqa: E501
    """get_notebook

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: ApiNotebook
    """
    return util.invoke_controller_impl()


def get_notebook_template(id):  # noqa: E501
    """get_notebook_template

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: ApiGetTemplateResponse
    """
    return util.invoke_controller_impl()


def list_notebooks(page_token=None, page_size=None, sort_by=None, filter=None):  # noqa: E501
    """list_notebooks

     # noqa: E501

    :param page_token: 
    :type page_token: str
    :param page_size: 
    :type page_size: int
    :param sort_by: Can be format of \&quot;field_name\&quot;, \&quot;field_name asc\&quot; or \&quot;field_name desc\&quot; Ascending by default.
    :type sort_by: str
    :param filter: A string-serialized JSON dictionary with key-value pairs that correspond to the Notebook&#39;s attribute names and their respective values to be filtered for.
    :type filter: str

    :rtype: ApiListNotebooksResponse
    """
    return util.invoke_controller_impl()


def run_notebook(id, run_name=None, parameters=None):  # noqa: E501
    """run_notebook

     # noqa: E501

    :param id: 
    :type id: str
    :param run_name: name to identify the run on the Kubeflow Pipelines UI, defaults to notebook name
    :type run_name: str
    :param parameters: optional run parameters, may be required based on pipeline definition
    :type parameters: dict | bytes

    :rtype: ApiRunCodeResponse
    """
    if connexion.request.is_json:
        parameters = Dictionary.from_dict(connexion.request.get_json())  # noqa: E501
    return util.invoke_controller_impl()


def set_featured_notebooks(notebook_ids):  # noqa: E501
    """set_featured_notebooks

     # noqa: E501

    :param notebook_ids: Array of notebook IDs to be featured.
    :type notebook_ids: List[]

    :rtype: None
    """
    return util.invoke_controller_impl()


def upload_notebook(uploadfile, name=None, enterprise_github_token=None):  # noqa: E501
    """upload_notebook

     # noqa: E501

    :param uploadfile: The notebook metadata YAML file to upload. Can be a GZip-compressed TAR file (.tgz, .tar.gz) or a YAML file (.yaml, .yml). Maximum size is 32MB.
    :type uploadfile: werkzeug.datastructures.FileStorage
    :param name: 
    :type name: str
    :param enterprise_github_token: Optional GitHub API token providing read-access to notebooks stored on Enterprise GitHub accounts.
    :type enterprise_github_token: str

    :rtype: ApiNotebook
    """
    return util.invoke_controller_impl()


def upload_notebook_file(id, uploadfile):  # noqa: E501
    """upload_notebook_file

     # noqa: E501

    :param id: The id of the notebook.
    :type id: str
    :param uploadfile: The file to upload, overwriting existing. Can be a GZip-compressed TAR file (.tgz), a YAML file (.yaml), Python script (.py), or Markdown file (.md)
    :type uploadfile: werkzeug.datastructures.FileStorage

    :rtype: ApiNotebook
    """
    return util.invoke_controller_impl()


def upload_notebook_from_url(url, name=None, access_token=None):  # noqa: E501
    """upload_notebook_from_url

     # noqa: E501

    :param url: URL pointing to the notebook YAML file.
    :type url: str
    :param name: Optional, the name of the notebook to be created overriding the name in the YAML file.
    :type name: str
    :param access_token: Optional, the Bearer token to access the &#39;url&#39;.
    :type access_token: str

    :rtype: ApiNotebook
    """
    return util.invoke_controller_impl()
