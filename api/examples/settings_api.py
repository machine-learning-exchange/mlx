# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0
from __future__ import print_function

import swagger_client

from pprint import pprint
from swagger_client.api_client import ApiClient, Configuration
from swagger_client.models import ApiSettings, ApiSettingsSection, ApiParameter
from swagger_client.rest import ApiException
from sys import stderr


host = '127.0.0.1'
port = '8080'
# host = env.get("MLX_API_SERVICE_HOST")
# port = env.get("MLX_API_SERVICE_PORT")

api_base_path = 'apis/v1alpha1'


def get_swagger_client():
    config = Configuration()
    config.host = f'http://{host}:{port}/{api_base_path}'
    api_client = ApiClient(configuration=config)
    return api_client


def print_function_name_decorator(func):
    def wrapper(*args, **kwargs):
        print()
        print(f"---[ {func.__name__}{args}{kwargs} ]---")
        print()
        return func(*args, **kwargs)
    return wrapper


@print_function_name_decorator
def get_app_settings():

    api_client = get_swagger_client()
    api_instance = swagger_client.ApplicationSettingsApi(api_client=api_client)

    try:
        api_settings: ApiSettings = api_instance.get_application_settings()
        pprint(api_settings, indent=2)
        return api_settings

    except ApiException as e:
        print(f"Exception when calling {api_instance.__class__.__name__}: %s\n" % e, file=stderr)
        raise e

    return None


@print_function_name_decorator
def modify_app_settings(dictionary: dict):

    api_client = get_swagger_client()
    api_instance = swagger_client.ApplicationSettingsApi(api_client=api_client)

    try:
        api_settings: ApiSettings = api_instance.modify_application_settings(dictionary)
        pprint(api_settings, indent=2)
        return api_settings

    except ApiException as e:
        print(f"Exception when calling {api_instance.__class__.__name__}: %s\n" % e, file=stderr)
        raise e

    return None


@print_function_name_decorator
def set_app_settings(api_settings: ApiSettings):

    api_client = get_swagger_client()
    api_instance = swagger_client.ApplicationSettingsApi(api_client=api_client)

    try:
        api_settings: ApiSettings = api_instance.set_application_settings(api_settings)
        pprint(api_settings, indent=2)
        return api_settings

    except ApiException as e:
        print(f"Exception when calling {api_instance.__class__.__name__}: %s\n" % e, file=stderr)
        raise e

    return None


def main():
    settings = get_app_settings()

    modify_app_settings({
        "Upload enabled": False,
        "API endpoint": "localhost:8080"
    })

    settings.sections += [
        ApiSettingsSection(
            name="General",
            description="General settings",
            settings=[
                ApiParameter("Color scheme", 'Color scheme [blue, red, yellow]', 'blue', 'red')
            ]
        )
    ]

    set_app_settings(settings)


if __name__ == '__main__':
    main()
