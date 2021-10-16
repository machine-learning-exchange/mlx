# Copyright 2021 The MLX Contributors
# 
# SPDX-License-Identifier: Apache-2.0

from kfserving import KFServingClient
import yaml


def get_kfserving_client():
    client = KFServingClient()
    return client


def get_all_services(name=None, namespace=None):
    client = get_kfserving_client()
    if not namespace:
        namespace = 'default'
    return client.get(name, namespace=namespace)


def post_service(inferenceservice=None, namespace=None):
    client = get_kfserving_client()
    service_dict = inferenceservice.to_dict()
    name = service_dict['metadata']['name']
    if not namespace:
        namespace = service_dict['metadata'].get('namespace', 'default')
    try:
        return client.create(service_dict, namespace=namespace)
    except:
        return client.patch(name, service_dict, namespace=namespace)


def from_client_upload_service(upload_file=None, namespace=None):
    client = get_kfserving_client()
    yaml_object = yaml.safe_load(upload_file)
    name = yaml_object['metadata']['name']
    if not namespace:
        namespace = yaml_object['metadata'].get('namespace', 'default')
    try:
        return client.create(yaml_object, namespace=namespace)
    except:
        return client.patch(name, yaml_object, namespace=namespace)
