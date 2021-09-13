# Copyright 2021 IBM Corporation
#
# SPDX-License-Identifier: Apache-2.0

import connexion
import six

from swagger_server.models.api_settings import ApiSettings  # noqa: E501
from swagger_server.models.api_status import ApiStatus  # noqa: E501
from swagger_server.models.dictionary import Dictionary  # noqa: E501
from swagger_server import util


def get_application_settings():  # noqa: E501
    """get_application_settings

    Returns the application settings. # noqa: E501


    :rtype: ApiSettings
    """
    return util.invoke_controller_impl()


def modify_application_settings(dictionary):  # noqa: E501
    """modify_application_settings

    Modify one or more of the application settings. # noqa: E501

    :param dictionary: A dictionary where the name of the keys corresponds to the name of the settings.
    :type dictionary: dict | bytes

    :rtype: ApiSettings
    """
    if connexion.request.is_json:
        dictionary = Dictionary.from_dict(connexion.request.get_json())  # noqa: E501
    return util.invoke_controller_impl()


def set_application_settings(settings):  # noqa: E501
    """set_application_settings

    Set and store the application settings. # noqa: E501

    :param settings: 
    :type settings: dict | bytes

    :rtype: ApiSettings
    """
    if connexion.request.is_json:
        settings = ApiSettings.from_dict(connexion.request.get_json())  # noqa: E501
    return util.invoke_controller_impl()
