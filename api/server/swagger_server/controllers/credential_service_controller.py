# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0

import connexion
import six

from swagger_server.models.api_credential import ApiCredential  # noqa: E501
from swagger_server.models.api_list_credentials_response import ApiListCredentialsResponse  # noqa: E501
from swagger_server.models.api_status import ApiStatus  # noqa: E501
from swagger_server import util


def create_credential(body):  # noqa: E501
    """create_credential

    Creates a credential associated with a pipeline. # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: ApiCredential
    """
    if connexion.request.is_json:
        body = ApiCredential.from_dict(connexion.request.get_json())  # noqa: E501
    return util.invoke_controller_impl()


def delete_credential(id):  # noqa: E501
    """delete_credential

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: None
    """
    return util.invoke_controller_impl()


def get_credential(id):  # noqa: E501
    """get_credential

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: ApiCredential
    """
    return util.invoke_controller_impl()


def list_credentials(page_token=None, page_size=None, sort_by=None, filter=None):  # noqa: E501
    """list_credentials

     # noqa: E501

    :param page_token: 
    :type page_token: str
    :param page_size: 
    :type page_size: int
    :param sort_by: Can be format of \&quot;field_name\&quot;, \&quot;field_name asc\&quot; or \&quot;field_name desc\&quot; Ascending by default.
    :type sort_by: str
    :param filter: A string-serialized JSON dictionary with key-value pairs that correspond to the Credential&#39;s attribute names and their respective values to be filtered for.
    :type filter: str

    :rtype: ApiListCredentialsResponse
    """
    return util.invoke_controller_impl()
