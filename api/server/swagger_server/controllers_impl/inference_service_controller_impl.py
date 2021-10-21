# Copyright 2019-2020 IBM Corporation
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

from swagger_server.models.api_inferenceservice import ApiInferenceservice  # noqa: E501
from swagger_server.models.api_list_inferenceservices_response import ApiListInferenceservicesResponse  # noqa: E501

from swagger_server.gateways.kfserving_client import get_all_services
from swagger_server.gateways.kfserving_client import post_service
from swagger_server.gateways.kfserving_client import from_client_upload_service

import logging


def get_inferenceservices(id, namespace=None):  # noqa: E501
    """get_inferenceservices

     # noqa: E501

    :param id: 
    :type id: str
    :param namespace: 
    :type namespace: str

    :rtype: ApiInferenceservice
    """
    log = logging.getLogger("inf_serv")
    # Attempt to find the id in a model mesh predictor
    try:
        single_service = get_all_services(id, namespace=namespace, group="serving.kserve.io", version="v1alpha1", plural="predictors")
        return single_service, 200
    except:
        pass
    # Attempt to find the id in a kserve inferenceservice
    try:
        single_service = get_all_services(id, namespace=namespace, group="serving.kserve.io", version="v1beta1", plural="inferenceservices")
        return single_service, 200
    except Exception as err:
        log.exception("Error when trying to find an inferenceservice: ")
        return str(err), 500


def list_inferenceservices(page_token=None, page_size=None, sort_by=None, filter=None, namespace=None):  # noqa: E501
    """list_inferenceservices

     # noqa: E501

    :param page_token: 
    :type page_token: str
    :param page_size: 
    :type page_size: int
    :param sort_by: Can be format of \&quot;field_name\&quot;, \&quot;field_name asc\&quot; or \&quot;field_name desc\&quot; Ascending by default.
    :type sort_by: str
    :param filter: A string-serialized JSON dictionary containing key-value pairs with name of the object property to apply filter on and the value of the respective property.
    :type filter: str
    :param namespace: 
    :type namespace: str

    :rtype: ApiListInferenceservicesResponse
    """
    log = logging.getLogger("inf_serv")
    try:
        # Combine the list of items from the modelmesh predictors and kserve inferenceservices
        all_mm_services = get_all_services(namespace=namespace, group="serving.kserve.io", version="v1alpha1", plural="predictors")
        all_k_services = get_all_services(namespace=namespace, group="serving.kserve.io", version="v1beta1", plural="inferenceservices")
        all_mm_services['items'] = all_mm_services['items'] + all_k_services['items']
        return all_mm_services, 200
    except Exception as err:
        log.exception("Error when trying to list inferenceservices: ")
        return str(err), 500


def create_service(body, namespace=None):  # noqa: E501
    """create_service

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param namespace: 
    :type namespace: str

    :rtype: ApiInferenceservice
    """
    log = logging.getLogger("inf_serv")
    try:
        created_service = post_service(body, namespace=namespace)
        return created_service, 200
    except Exception as err:
        log.exception("Error when deploying an inferenceservice: ")
        return str(err), 500


def upload_service(uploadfile, name=None, namespace=None):  # noqa: E501
    """upload_service

     # noqa: E501

    :param uploadfile: The component to upload. Maximum size of 32MB is supported.
    :type uploadfile: werkzeug.datastructures.FileStorage
    :param name: 
    :type name: str
    :param namespace: 
    :type namespace: str

    :rtype: ApiComponent
    """
    log = logging.getLogger("inf_serv")
    try:
        uploaded_service = from_client_upload_service(upload_file=uploadfile, namespace=namespace)
        return uploaded_service, 200
    except Exception as err:
        log.exception("Error when deploying an inferenceservice: ")
        return str(err), 500

