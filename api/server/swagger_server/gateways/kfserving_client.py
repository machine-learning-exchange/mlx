# Copyright 2019-2020 IBM Corporation
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