# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0

import connexion
import six

from swagger_server.models.api_dataset import ApiDataset  # noqa: E501
from swagger_server.models.api_generate_code_response import ApiGenerateCodeResponse  # noqa: E501
from swagger_server.models.api_get_template_response import ApiGetTemplateResponse  # noqa: E501
from swagger_server.models.api_list_datasets_response import ApiListDatasetsResponse  # noqa: E501
from swagger_server.models.api_parameter import ApiParameter  # noqa: E501
from swagger_server.models.api_run_code_response import ApiRunCodeResponse  # noqa: E501
from swagger_server.models.api_status import ApiStatus  # noqa: E501
from swagger_server import util


def approve_datasets_for_publishing(dataset_ids):  # noqa: E501
    """approve_datasets_for_publishing

     # noqa: E501

    :param dataset_ids: Array of dataset IDs to be approved for publishing.
    :type dataset_ids: List[str]

    :rtype: None
    """
    return util.invoke_controller_impl()


def create_dataset(body):  # noqa: E501
    """create_dataset

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: ApiDataset
    """
    if connexion.request.is_json:
        body = ApiDataset.from_dict(connexion.request.get_json())  # noqa: E501
    return util.invoke_controller_impl()


def delete_dataset(id):  # noqa: E501
    """delete_dataset

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: None
    """
    return util.invoke_controller_impl()


def download_dataset_files(id, include_generated_code=None):  # noqa: E501
    """Returns the dataset artifacts compressed into a .tgz (.tar.gz) file.

     # noqa: E501

    :param id: 
    :type id: str
    :param include_generated_code: Include generated run script in download
    :type include_generated_code: bool

    :rtype: file | binary
    """
    return util.invoke_controller_impl()


def generate_dataset_code(id):  # noqa: E501
    """generate_dataset_code

    Generate sample code to use dataset in a pipeline # noqa: E501

    :param id: 
    :type id: str

    :rtype: ApiGenerateCodeResponse
    """
    return util.invoke_controller_impl()


def get_dataset(id):  # noqa: E501
    """get_dataset

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: ApiDataset
    """
    return util.invoke_controller_impl()


def get_dataset_template(id):  # noqa: E501
    """get_dataset_template

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: ApiGetTemplateResponse
    """
    return util.invoke_controller_impl()


def list_datasets(page_token=None, page_size=None, sort_by=None, filter=None):  # noqa: E501
    """list_datasets

     # noqa: E501

    :param page_token: 
    :type page_token: str
    :param page_size: 
    :type page_size: int
    :param sort_by: Can be format of &#39;field_name&#39;, &#39;field_name asc&#39; or &#39;field_name desc&#39;. Ascending by default.
    :type sort_by: str
    :param filter: A string-serialized JSON dictionary containing key-value pairs with name of the object property to apply filter on and the value of the respective property.
    :type filter: str

    :rtype: ApiListDatasetsResponse
    """
    return util.invoke_controller_impl()


def run_dataset(id, parameters=None, run_name=None):  # noqa: E501
    """run_dataset

     # noqa: E501

    :param id: 
    :type id: str
    :param parameters: 
    :type parameters: list | bytes
    :param run_name: name to identify the run on the Kubeflow Pipelines UI, defaults to component name
    :type run_name: str

    :rtype: ApiRunCodeResponse
    """
    if connexion.request.is_json:
        parameters = [ApiParameter.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
    return util.invoke_controller_impl()


def set_featured_datasets(dataset_ids):  # noqa: E501
    """set_featured_datasets

     # noqa: E501

    :param dataset_ids: Array of dataset IDs to be featured.
    :type dataset_ids: List[str]

    :rtype: None
    """
    return util.invoke_controller_impl()


def upload_dataset(uploadfile, name=None):  # noqa: E501
    """upload_dataset

     # noqa: E501

    :param uploadfile: The dataset YAML file to upload. Can be a GZip-compressed TAR file (.tgz, .tar.gz) or a YAML file (.yaml, .yml). Maximum size is 32MB.
    :type uploadfile: werkzeug.datastructures.FileStorage
    :param name: 
    :type name: str

    :rtype: ApiDataset
    """
    return util.invoke_controller_impl()


def upload_dataset_file(id, uploadfile):  # noqa: E501
    """upload_dataset_file

     # noqa: E501

    :param id: The id of the dataset.
    :type id: str
    :param uploadfile: The file to upload, overwriting existing. Can be a GZip-compressed TAR file (.tgz), a YAML file (.yaml), Python script (.py), or Markdown file (.md)
    :type uploadfile: werkzeug.datastructures.FileStorage

    :rtype: ApiDataset
    """
    return util.invoke_controller_impl()


def upload_dataset_from_url(url, name=None, access_token=None):  # noqa: E501
    """upload_dataset_from_url

     # noqa: E501

    :param url: URL pointing to the dataset YAML file.
    :type url: str
    :param name: Optional, the name of the dataset to be created overriding the name in the YAML file.
    :type name: str
    :param access_token: Optional, the Bearer token to access the &#39;url&#39;.
    :type access_token: str

    :rtype: ApiDataset
    """
    return util.invoke_controller_impl()
