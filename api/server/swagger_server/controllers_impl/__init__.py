# Copyright 2021 The MLX Contributors
# 
# SPDX-License-Identifier: Apache-2.0

import requests

from werkzeug.datastructures import FileStorage

from kfp_tekton.compiler._k8s_helper import sanitize_k8s_name;
from swagger_server.data_access.minio_client import extract_yaml_from_tarfile
from swagger_server.models.api_parameter import ApiParameter
from swagger_server.util import ApiError


###############################################################################
#   private helper methods, not swagger-generated
# TODO: move into controllers_impl/util.py
###############################################################################

def get_yaml_file_content_from_uploadfile(uploadfile: FileStorage):

    file_name = uploadfile.filename
    file_ext = file_name.lower().split(".")[-1]

    if file_ext in ["tgz", "gz"]:
        yaml_file_content = extract_yaml_from_tarfile(uploadfile)

    elif file_ext in ["yaml", "yml"]:
        yaml_file_content = uploadfile.stream.read()

    else:
        raise ApiError(
            f"File extension not supported: '{file_ext}', uploadfile: '{file_name}'."
            f"Supported file extensions: .tar.gz, .gz, .yaml, .yml", 501)

    return yaml_file_content


def validate_parameters(api_parameters: [ApiParameter], parameters: dict) -> (str, int):

    acceptable_parameters = [p.name for p in api_parameters]
    unexpected_parameters = set(parameters.keys()) - set(acceptable_parameters)

    if unexpected_parameters:
        return f"Unexpected parameter(s): {list(unexpected_parameters)}. " \
               f"Acceptable parameter(s): {acceptable_parameters}", 422

    missing_parameters = [p.name for p in api_parameters
                          if not p.default and p.name not in parameters]

    if missing_parameters:
        return f"Missing required parameter(s): {missing_parameters}", 422

    return None, 200


def validate_id(id: str) -> (str, int):

    if id != sanitize_k8s_name(id):
        return f"Identifiers must contain lower case alphanumeric characters or '-' only.", 422

    return None, 200


def download_file_content_from_url(url: str, bearer_token: str = None) -> bytes:

    request_headers = dict()

    if bearer_token and "?token=" not in url:
        request_headers.update({"Authorization": f"Bearer {bearer_token}"})

    try:
        raw_url = url.replace("/blob/", "/") \
            .replace("/github.ibm.com/", "/raw.github.ibm.com/") \
            .replace("/github.com/", "/raw.githubusercontent.com/")

        response = requests.get(raw_url, allow_redirects=True, headers=request_headers)

        if response.ok:
            file_content = response.content
            return file_content

    except Exception as e:
        raise ApiError(f"Could not download file '{url}'. \n{str(e)}", 422)

    raise ApiError(f"Could not download file '{url}'. Reason: {response.reason}",
                   response.status_code)
