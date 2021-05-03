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
import yaml

from os.path import abspath, join, dirname
from swagger_server.models.api_parameter import ApiParameter  # noqa: E501
from swagger_server.models.api_settings import ApiSettings  # noqa: E501
from swagger_server.models.api_settings_section import ApiSettingsSection  # noqa: E501
from swagger_server.models.api_status import ApiStatus  # noqa: E501
from swagger_server import util


SETTINGS_FILE = abspath(join(dirname(__file__), "..", "..", "application_settings.yaml"))


def get_application_settings():  # noqa: E501
    """get_application_settings

    Returns the application settings.

    :rtype: ApiSettings
    """
    with open(SETTINGS_FILE, "r") as f:
        yaml_dict = yaml.load(f, Loader=yaml.FullLoader)

    settings = ApiSettings.from_dict(yaml_dict)

    return settings, 200


def modify_application_settings(dictionary: dict):  # noqa: E501
    """modify_application_settings

    Modify one or more of the application settings.

    :param dictionary: A dictionary where the name of the keys corresponds to the name of the settings.
    :type dictionary:

    :rtype: ApiSettings
    """
    with open(SETTINGS_FILE, "r") as f:
        yaml_dict = yaml.load(f, Loader=yaml.FullLoader)

    settings = ApiSettings.from_dict(yaml_dict)

    for section in settings.sections:
        for setting in section.settings:
            if setting.name in dictionary.keys():
                setting.value = dictionary.get(setting.name)

    with open(SETTINGS_FILE, 'w') as f:
        yaml.dump(settings.to_dict(), f, default_flow_style=False)

    return settings, 200


def set_application_settings(settings):  # noqa: E501
    """set_application_settings

    Set and store the application settings.

    :param settings:
    :type settings: dict

    :rtype: ApiSettings
    """
    if connexion.request.is_json:
        settings = ApiSettings.from_dict(connexion.request.get_json())

    with open(SETTINGS_FILE, 'w') as f:
        yaml.dump(settings.to_dict(), f, default_flow_style=False)

    return settings, 200
