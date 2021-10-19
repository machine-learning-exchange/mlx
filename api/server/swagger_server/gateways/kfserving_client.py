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
import logging


def get_all_services(name=None, namespace=None):

    log = logging.getLogger("inf_serv")
    if not namespace:
        namespace = 'default'

    config.load_incluster_config()
    api = client.CustomObjectsApi()
    if name is None:
        resource = api.list_namespaced_custom_object(
            group="serving.kserve.io",
            version="v1alpha1",
            namespace=namespace,
            plural="predictors",
        )
    else:
        resource = api.get_namespaced_custom_object(
            group="serving.kserve.io",
            version="v1alpha1",
            namespace=namespace,
            name=name,
            plural="predictors",
        )
    return resource


def post_service(inferenceservice=None, namespace=None):
    
    log = logging.getLogger("inf_serv")
    config.load_incluster_config()
    api = client.CustomObjectsApi() 

    service_dict = inferenceservice.to_dict()
    if not namespace:
        namespace = service_dict['metadata'].get('namespace', 'default')

    try:
        # create the resource
        api.create_namespaced_custom_object(
            group="serving.kserve.io",
            version="v1alpha1",
            namespace=namespace,
            plural="predictors",
            body=service_dict,
        )
    except:
        # If the creating the resource fails, try patching the resource
        log.info("Creation failed: Attempting to patch the resource.")
        api.patch_namespaced_custom_object(
            group="serving.kserve.io",
            version="v1alpha1",
            namespace=namespace,
            plural="predictors",
            body=service_dict,
        )


def from_client_upload_service(upload_file=None, namespace=None):

    log = logging.getLogger("inf_serv")
    config.load_incluster_config()
    api = client.CustomObjectsApi()

    yaml_object = yaml.safe_load(upload_file)
    if not namespace:
        namespace = yaml_object['metadata'].get('namespace', 'default')

    try:
        # create the resource
        api.create_namespaced_custom_object(
            group="serving.kserve.io",
            version="v1alpha1",
            namespace=namespace,
            plural="predictors",
            body=yaml_object,
        )
    except Exception as err:
        # If the creating the resource fails, try patching the resource
        log.info("Creation failed: Attempting to patch the resource.")
        api.patch_namespaced_custom_object(
            group="serving.kserve.io",
            version="v1alpha1",
            namespace=namespace,
            plural="predictors",
            body=yaml_object,
        )