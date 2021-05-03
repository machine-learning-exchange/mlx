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
import six

from swagger_server.models.api_component import ApiComponent  # noqa: E501
from swagger_server.models.api_generate_code_response import ApiGenerateCodeResponse  # noqa: E501
from swagger_server.models.api_get_template_response import ApiGetTemplateResponse  # noqa: E501
from swagger_server.models.api_list_components_response import ApiListComponentsResponse  # noqa: E501
from swagger_server.models.api_parameter import ApiParameter  # noqa: E501
from swagger_server.models.api_run_code_response import ApiRunCodeResponse  # noqa: E501
from swagger_server.models.api_status import ApiStatus  # noqa: E501
from swagger_server import util


def approve_components_for_publishing(component_ids):  # noqa: E501
    """approve_components_for_publishing

     # noqa: E501

    :param component_ids: Array of component IDs to be approved for publishing.
    :type component_ids: List[]

    :rtype: None
    """
    return util.invoke_controller_impl()


def create_component(body):  # noqa: E501
    """create_component

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: ApiComponent
    """
    if connexion.request.is_json:
        body = ApiComponent.from_dict(connexion.request.get_json())  # noqa: E501
    return util.invoke_controller_impl()


def delete_component(id):  # noqa: E501
    """delete_component

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: None
    """
    return util.invoke_controller_impl()


def download_component_files(id, include_generated_code=None):  # noqa: E501
    """Returns the component artifacts compressed into a .tgz (.tar.gz) file.

     # noqa: E501

    :param id: 
    :type id: str
    :param include_generated_code: Include generated run script in download
    :type include_generated_code: bool

    :rtype: file | binary
    """
    return util.invoke_controller_impl()


def generate_component_code(id):  # noqa: E501
    """generate_component_code

    Generate sample code to use component in a pipeline # noqa: E501

    :param id: 
    :type id: str

    :rtype: ApiGenerateCodeResponse
    """
    return util.invoke_controller_impl()


def get_component(id):  # noqa: E501
    """get_component

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: ApiComponent
    """
    return util.invoke_controller_impl()


def get_component_template(id):  # noqa: E501
    """get_component_template

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: ApiGetTemplateResponse
    """
    return util.invoke_controller_impl()


def list_components(page_token=None, page_size=None, sort_by=None, filter=None):  # noqa: E501
    """list_components

     # noqa: E501

    :param page_token: 
    :type page_token: str
    :param page_size: 
    :type page_size: int
    :param sort_by: Can be format of \&quot;field_name\&quot;, \&quot;field_name asc\&quot; or \&quot;field_name desc\&quot; Ascending by default.
    :type sort_by: str
    :param filter: A string-serialized JSON dictionary with key-value pairs that correspond to the ApiComponent&#39;s attribute names and their respective values to be filtered for.
    :type filter: str

    :rtype: ApiListComponentsResponse
    """
    return util.invoke_controller_impl()


def run_component(id, parameters, run_name=None):  # noqa: E501
    """run_component

     # noqa: E501

    :param id: 
    :type id: str
    :param parameters: 
    :type parameters: List[ApiParameter]
    :param run_name: name to identify the run on the Kubeflow Pipelines UI, defaults to component name
    :type run_name: str

    :rtype: ApiRunCodeResponse
    """
    if connexion.request.is_json:
        parameters = [ApiParameter.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
    return util.invoke_controller_impl()


def set_featured_components(component_ids):  # noqa: E501
    """set_featured_components

     # noqa: E501

    :param component_ids: Array of component IDs to be featured.
    :type component_ids: List[]

    :rtype: None
    """
    return util.invoke_controller_impl()


def upload_component(uploadfile, name=None):  # noqa: E501
    """upload_component

     # noqa: E501

    :param uploadfile: The component YAML file to upload. Can be a GZip-compressed TAR file (.tgz, .tar.gz) or a YAML file (.yaml, .yml). Maximum size is 32MB.
    :type uploadfile: werkzeug.datastructures.FileStorage
    :param name: 
    :type name: str

    :rtype: ApiComponent
    """
    return util.invoke_controller_impl()


def upload_component_file(id, uploadfile):  # noqa: E501
    """upload_component_file

     # noqa: E501

    :param id: The id of the component.
    :type id: str
    :param uploadfile: The file to upload, overwriting existing. Can be a GZip-compressed TAR file (.tgz), a YAML file (.yaml), Python script (.py), or Markdown file (.md)
    :type uploadfile: werkzeug.datastructures.FileStorage

    :rtype: ApiComponent
    """
    return util.invoke_controller_impl()


def upload_component_from_url(url, name=None, access_token=None):  # noqa: E501
    """upload_component_from_url

     # noqa: E501

    :param url: URL pointing to the component YAML file.
    :type url: str
    :param name: Optional, the name of the component to be created overriding the name in the YAML file.
    :type name: str
    :param access_token: Optional, the Bearer token to access the &#39;url&#39;.
    :type access_token: str

    :rtype: ApiComponent
    """
    return util.invoke_controller_impl()
