# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0

import json
import subprocess

from base64 import b64decode
from os import environ as env
from pprint import pprint
from swagger_server.util import ApiError


secret_name_prefix = "mlx-pipeline-creds"

_namespace = env.get("POD_NAMESPACE", "kubeflow")


def create_secret(secret_name: str, secret_contents: dict):
    try:
        command = ['kubectl', '-n', _namespace, 'create', 'secret', 'generic', secret_name]
        for key, value in secret_contents.items():
            if type(value) == dict:
                raise ApiError(f"Secret values must not be of type 'dict'")
            if type(value) == list:
                value = ",".join([str(v) for v in value])
            if type(value) == str and " " in value:
                value = f"\"{value}\""
            command.append(f"--from-literal={key}={value or ''}")
        output = subprocess.run(command, capture_output=True, check=True, timeout=10)
        pprint(output.stdout.decode())
    except Exception as e:
        if output and output.stderr:
            pprint(output.stderr.decode())
        raise ApiError(f"Error trying to create secret '{secret_name}': {e}")


def delete_secret(secret_name):
    if secret_name == "*":
        return delete_all_secrets()
    output = None
    try:
        delete_command = ['kubectl', 'delete', '-n', _namespace, 'secret', secret_name]
        output = subprocess.run(delete_command, capture_output=True, check=True, timeout=10)
        print(f"Credential {secret_name} was deleted")
    except Exception as e:
        if output and output.stderr:
            pprint(output.stderr.decode())
        raise ApiError(f"Error trying to delete secret '{secret_name}': {e}")


def delete_all_secrets(name_prefix=secret_name_prefix):
    secrets = list_secrets(name_prefix=name_prefix)
    for secret in secrets:
        secret_name = secret["metadata"]["name"]
        delete_secret(secret_name)


def get_secret(secret_name, decode=False) -> dict:
    output = None
    try:
        get_command = ['kubectl', '-n', _namespace, '-o', 'json', 'get', 'secret', secret_name]
        output = subprocess.run(get_command, capture_output=True, check=True, timeout=10)
        secret_data = json.loads(output.stdout.decode()) or {}
        secret = secret_data.get("data")
        if decode:
            for k, v in secret.items():
                secret[k] = b64decode(v).decode()
        return secret
    except Exception as e:
        if output and output.stderr:
            pprint(output.stderr.decode())
        raise ApiError( f"Error trying to retrieve secret '{secret_name}': {e}")


def list_secrets(name_prefix=secret_name_prefix, decode=False) -> [dict]:
    output = None
    try:
        list_command = ['kubectl', '-n', _namespace,  '-o', 'json', 'get', 'secrets']
        output = subprocess.run(list_command, capture_output=True, check=True, timeout=10)
        secrets_data = json.loads(output.stdout.decode()) or {}
        mlx_secrets = [d for d in secrets_data.get("items") or []
                             if d["metadata"]["name"].startswith(name_prefix)]
        if decode:
            for s in mlx_secrets:
                for k, v in s["data"].items():
                    s["data"][k] = b64decode(v).decode()
        return mlx_secrets
    except Exception as e:
        if output and output.stderr:
            pprint(output.stderr.decode())
        raise ApiError(f"Error trying to list secrets '{name_prefix}...': {e}")
