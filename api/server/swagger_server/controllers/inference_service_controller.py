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

from swagger_server.models.api_inferenceservice import ApiInferenceservice  # noqa: E501
from swagger_server.models.api_list_inferenceservices_response import ApiListInferenceservicesResponse  # noqa: E501
from swagger_server.models.api_status import ApiStatus  # noqa: E501
from swagger_server import util


def create_service(body, namespace=None):  # noqa: E501
    """create_service

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param namespace: 
    :type namespace: str

    :rtype: ApiInferenceservice
    """
    if connexion.request.is_json:
        body = ApiInferenceservice.from_dict(connexion.request.get_json())  # noqa: E501
    return util.invoke_controller_impl()


def get_inferenceservices(id, namespace=None):  # noqa: E501
    """get_inferenceservices

     # noqa: E501

    :param id: 
    :type id: str
    :param namespace: 
    :type namespace: str

    :rtype: ApiInferenceservice
    """
    return util.invoke_controller_impl()


def list_inferenceservices(page_token=None, page_size=None, sort_by=None, filter=None, namespace=None):  # noqa: E501
    """list_inferenceservices

     # noqa: E501

    :param page_token: 
    :type page_token: str
    :param page_size: 
    :type page_size: int
    :param sort_by: Can be format of \&quot;field_name\&quot;, \&quot;field_name asc\&quot; or \&quot;field_name desc\&quot; Ascending by default.
    :type sort_by: str
    :param filter: A string-serialized JSON dictionary with key-value pairs that correspond to the InferenceService&#39;s attribute names and their respective values to be filtered for.
    :type filter: str
    :param namespace: 
    :type namespace: str

    :rtype: ApiListInferenceservicesResponse
    """
    return util.invoke_controller_impl()


def upload_service(uploadfile, name=None, namespace=None):  # noqa: E501
    """upload_service

     # noqa: E501

    :param uploadfile: The inference service metadata to upload. Maximum size of 32MB is supported.
    :type uploadfile: werkzeug.datastructures.FileStorage
    :param name: 
    :type name: str
    :param namespace: 
    :type namespace: str

    :rtype: ApiInferenceservice
    """
    return util.invoke_controller_impl()
