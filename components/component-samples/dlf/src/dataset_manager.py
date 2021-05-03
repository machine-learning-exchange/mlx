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
import json
import argparse
import os
import requests
import re
import time
import yaml
from distutils.util import strtobool
from kubernetes import config, client


def yamlStr(str):
    if str == "" or str == None:
        return None
    else:
        return yaml.safe_load(str)


def get_custom_objects_api_client():
    try:
        config.load_kube_config()
    except:
        config.load_incluster_config()
    api_client = client.CustomObjectsApi()
    return api_client


def get_corev1_api_client():
    try:
        config.load_kube_config()
    except:
        config.load_incluster_config()
    api_client = client.CoreV1Api()
    return api_client


def run_dlf(action, dataset_yaml, namespace=None):
    api_client = get_custom_objects_api_client()
    ## Check provided yaml
    try:
        name = dataset_yaml['metadata']['name']
        namespace = namespace or dataset_yaml['metadata'].get('namespace', 'default')
        group, version = dataset_yaml["apiVersion"].split("/")
        plural = dataset_yaml["kind"].lower()+"s"
    except:
        print("The provided yaml doesn't match with the DLF standard")
        raise
    if plural != 'datasets':
        print("The provided yaml is not a dataset")
        exit(1)
    if not namespace:
        print("Warning: Namespace is missing, using 'default'\n")

    ## Perform actions
    api_response = api_client.list_namespaced_custom_object(group=group,
                                                            version=version,
                                                            namespace=namespace,
                                                            plural=plural)
    is_dataset_exist = name in [deployment["metadata"]["name"] for deployment in api_response["items"]]
    if action == "create":
        if is_dataset_exist:
            print("Dataset %s already exist. Datasets are immutable objects so they cannot be recreated" % name)
            exit(0)
        else:
            return api_client.create_namespaced_custom_object(group=group,
                                                              version=version,
                                                              namespace=namespace,
                                                              plural=plural,
                                                              body=dataset_yaml)
    if action == "delete":
        from kubernetes.client import V1DeleteOptions
        if not is_dataset_exist:
            print("Dataset %s already deleted. Not action is performed" % name)
            return None
        else:
            delete_results = api_client.delete_namespaced_custom_object(group=group,
                                                                        version=version,
                                                                        namespace=namespace,
                                                                        plural=plural,
                                                                        name=name,
                                                                        body=V1DeleteOptions())
            print("Dataset %s is deleted." % name)
            return delete_results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--action",
        type=str,
        help="Action to execute on DLF",
        default="create"
    )
    parser.add_argument(
        "--output-path",
        type=str,
        help="Path to store status output"
    )
    parser.add_argument(
        "--dataset_yaml",
        type=yamlStr,
        help="Raw Dataset serialized YAML for deployment",
        default={}
    )
    parser.add_argument(
        "--namespace",
        type=str,
        help="Kubernetes namespace for deployment",
        default="default"
    )

    ### Argument variables
    args = parser.parse_args()
    action = args.action.lower()
    output_path = args.output_path
    dataset_yaml = args.dataset_yaml
    namespace = args.namespace

    ### Run DLF yaml
    status = run_dlf(action, dataset_yaml, namespace)
    if action == "delete":
        status = {}
    else:
        if status.get('metadata', "failed") == "failed":
            print("Dataset wasn't deployed sucessfully. Please check the DLF controller for more details.")
            exit(1)
        name = status['metadata']['name']
        namespace = status['metadata']['namespace']
        v1_client = get_corev1_api_client()
        bounded = False
        for i in range(24):
            try:
                pvc_spec = v1_client.read_namespaced_persistent_volume_claim(name=name, namespace=namespace)
                if pvc_spec.status.phase == 'Bound':
                    print("Dataset %s is bounded" % name)
                    bounded = True
                    break
                print("Waiting for %s to be ready: %ss" % (name, str(i*5)))
                time.sleep(5)
            except:
                print("Wating for pvc spec: %ss" % str(i*5))
                time.sleep(5)
                continue
        if not bounded:
            print("Dataset %s has been timeout and is not ready. Please check the DLF controller for more details." % name)
            exit(1)


    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))
    with open(output_path, "w") as report:
        report.write(json.dumps(status))
