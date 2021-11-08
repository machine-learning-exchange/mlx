# Copyright 2021 The MLX Contributors
# 
# SPDX-License-Identifier: Apache-2.0

import yaml
from kubernetes import client, config


def get_all_services(name=None, namespace=None, group=None, version=None, plural=None):

    config.load_incluster_config()
    api = client.CustomObjectsApi()

    if not namespace:
        namespace = 'default'

    if name is None:
        resource = api.list_namespaced_custom_object(
            group=group,
            version=version,
            namespace=namespace,
            plural=plural,
        )
    else:
        resource = api.get_namespaced_custom_object(
            group=group,
            version=version,
            namespace=namespace,
            name=name,
            plural=plural,
        )
    return resource


def post_service(inferenceservice=None, namespace=None, group=None, version=None, plural=None):

    config.load_incluster_config()
    api = client.CustomObjectsApi() 

    service_dict = inferenceservice.to_dict()
    # Get resource information from the dict
    version_split = service_dict['apiVersion'].split("/")
    group = version_split[0]
    version = version_split[1]
    plural = service_dict['kind'].lower() + "s"
    if not namespace:
        namespace = service_dict['metadata'].get('namespace', 'default')

    # create the resource
    ns_obj = api.create_namespaced_custom_object(
        group=group,
        version=version,
        namespace=namespace,
        plural=plural,
        body=service_dict,
    )
    return ns_obj


def from_client_upload_service(upload_file=None, namespace=None, group=None, version=None, plural=None):

    config.load_incluster_config()
    api = client.CustomObjectsApi()

    yaml_object = yaml.safe_load(upload_file)
    # Get resource information from the yaml
    name = yaml_object['metadata']['name']
    version_split = yaml_object['apiVersion'].split("/")
    group = version_split[0]
    version = version_split[1]
    plural = yaml_object['kind'].lower() + "s"
    if not namespace:
        namespace = yaml_object['metadata'].get('namespace', 'default')

    # create the resource
    ns_obj = api.create_namespaced_custom_object(
        group=group,
        version=version,
        namespace=namespace,
        plural=plural,
        body=yaml_object,
    )
    return ns_obj