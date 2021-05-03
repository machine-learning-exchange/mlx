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
