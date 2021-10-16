# Copyright 2021 The MLX Contributors
# 
# SPDX-License-Identifier: Apache-2.0

from swagger_server.models.api_inferenceservice import ApiInferenceservice  # noqa: E501
from swagger_server.models.api_list_inferenceservices_response import ApiListInferenceservicesResponse  # noqa: E501

from swagger_server.gateways.kfserving_client import get_all_services
from swagger_server.gateways.kfserving_client import post_service
from swagger_server.gateways.kfserving_client import from_client_upload_service


def get_inferenceservices(id, namespace=None):  # noqa: E501
    """get_inferenceservices

     # noqa: E501

    :param id: 
    :type id: str
    :param namespace: 
    :type namespace: str

    :rtype: ApiInferenceservice
    """
    single_service = get_all_services(id, namespace=namespace)
    return single_service, 200


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
    all_services = get_all_services(namespace=namespace)
    return all_services, 200


def create_service(body, namespace=None):  # noqa: E501
    """create_service

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param namespace: 
    :type namespace: str

    :rtype: ApiInferenceservice
    """
    created_service = post_service(body, namespace=namespace)
    return created_service, 200


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
    uploaded_service = from_client_upload_service(uploadfile, namespace=namespace)
    return uploaded_service, 200
