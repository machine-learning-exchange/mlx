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
import os

import json
import logging
import re
import requests
import sys
import traceback

from flask import Flask, request, abort
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# Setup Logging
logging.basicConfig(level="INFO", format='%(levelname)s: %(message)s')

LOG = logging.getLogger("deploy_model")


def load_kube_config(params):
    from kubernetes import config

    config.load_incluster_config()


def get_api_client_v1():
    import kubernetes
    api_client_v1 = kubernetes.client.CoreV1Api()
    return api_client_v1


def get_custom_objects_api_client():
    import kubernetes
    api_client = kubernetes.client.CustomObjectsApi()
    return api_client

def get_api_client_appv1():
    import kubernetes
    api_client = kubernetes.client.AppsV1Api()
    return api_client


def get_deployment_spec(params):
    with open("kube/deployment.json") as f:
        spec = json.load(f)
    deployment_name = get_deployment_name(params)
    spec["metadata"]["name"] = deployment_name
    return spec


def get_service_spec():
    with open("kube/service.json") as f:
        spec = json.load(f)
    return spec


def update_deployment_spec(params):
    spec = get_deployment_spec(params)

    if "container_image" in params:
        spec["spec"]["template"]["spec"]["containers"][0]["image"] = params["container_image"]

    spec["metadata"]["name"] = params["deployment_name"]
    spec["metadata"]["labels"]["app"] = params["deployment_name"]
    spec["spec"]["selector"]["matchLabels"]["app"] = params["deployment_name"]
    spec["spec"]["template"]["metadata"]["labels"]["app"] = params["deployment_name"]

    spec["spec"]["template"]["spec"]["containers"][0]["ports"][0]["containerPort"] = int(params["container_port"])

    spec["spec"]["template"]["spec"]["containers"][0]["env"] = json.loads(params["env_vars"])

    return spec


def deploy_deployment_spec(spec, params):

    name = spec["metadata"]["name"]
    namespace = params["namespace"]

    api_client = get_api_client_appv1()
    api_response = api_client.list_namespaced_deployment(namespace)

    if name in [deployment.metadata.name for deployment in api_response.items]:
        api_response = api_client.patch_namespaced_deployment(name, namespace, spec)
    else:
        api_response = api_client.create_namespaced_deployment(namespace, spec)

    # api_response_filtered = {key: api_response[key] for key in ["apiVersion", "kind"]}
    LOG.info("%s ..." % str(api_response)[:160])
    return api_response


def deploy_service_spec(params):

    spec = get_service_spec()
    name = params["deployment_name"]
    namespace = params["namespace"]

    spec["metadata"]["name"] = params["deployment_name"]
    spec["metadata"]["labels"]["app"] = params["deployment_name"]
    spec["spec"]["selector"]["app"] = params["deployment_name"]
    spec["spec"]["ports"][0]["port"] = int(params["container_port"])

    api_client = get_api_client_v1()
    api_response = api_client.list_namespaced_service(namespace)

    if name in [service.metadata.name for service in api_response.items]:
        api_response = api_client.patch_namespaced_service(name, namespace, spec)
    else:
        api_response = api_client.create_namespaced_service(namespace, spec)

    # api_response_filtered = {key: api_response[key] for key in ["apiVersion", "kind"]}
    LOG.info("%s ..." % str(api_response)[:160])
    return api_response


def delete_serving_deployment(params):
    from kubernetes.client import V1DeleteOptions

    spec = get_deployment_spec(params)
    name = params["deployment_name"]
    namespace = params["namespace"]

    spec["metadata"]["name"] = params["deployment_name"]
    spec["metadata"]["labels"]["app"] = params["deployment_name"]
    spec["spec"]["selector"]["matchLabels"]["app"] = params["deployment_name"]
    spec["spec"]["template"]["metadata"]["labels"]["app"] = params["deployment_name"]

    del_opts = V1DeleteOptions()
    api_client = get_api_client_appv1()
    api_response = api_client.list_namespaced_deployment(namespace)

    if name in [deployment.metadata.name for deployment in api_response.items]:
        api_response = api_client.delete_namespaced_deployment(name, namespace, body=del_opts)
    else:
        LOG.error("Could not find the serving deployment '%s'" % name)
        return {
            "status": "Error",
            "details": "Could not find a serving deployment with name '%s'" % name
        }

    # api_response_filtered = {key: api_response[key] for key in ["apiVersion", "kind"]}
    LOG.info("%s ..." % str(api_response)[:160])
    return api_response


def delete_serving_service(params):
    from kubernetes.client import V1DeleteOptions

    spec = get_service_spec()
    name = params["deployment_name"]
    namespace = params["namespace"]

    spec["metadata"]["name"] = params["deployment_name"]
    spec["metadata"]["labels"]["app"] = params["deployment_name"]
    spec["spec"]["selector"]["app"] = params["deployment_name"]
    spec["spec"]["ports"][0]["port"] = int(params["container_port"])

    del_opts = V1DeleteOptions()
    api_client = get_api_client_v1()
    api_response = api_client.list_namespaced_service(namespace)

    if name in [service.metadata.name for service in api_response.items]:
        api_response = api_client.delete_namespaced_service(name, namespace, body=del_opts)
    else:
        LOG.error("Could not find the serving service '%s'" % name)
        return {
            "status": "Error",
            "details": "Could not find a serving service with name '%s'" % name
        }

    # api_response_filtered = {key: api_response[key] for key in ["apiVersion", "kind"]}
    LOG.info("%s ..." % str(api_response)[:160])
    return api_response


def get_deployment_status(params):
    # AVAILABLE (classifier URL actually available)
    # READY (pod status, not url availability)
    # UNKNOWN (no pods)
    # ERROR (CrashLoopBackOff, Succeeded - if pod terminated, will not be restarted, this should not happen)
    # PENDING (Creating..., ContainerCreating, ContainersReady, PodScheduled, Pending, Initialized, Running)
    status = get_serving_deployment_state(params) or "Unknown"

    return status.upper()


def get_serving_deployment_state(params):
    deployment_name = get_deployment_name(params)
    spec = get_deployment_spec(params)
    namespace = params["namespace"]
    api_client = get_api_client_appv1()
    api_response = api_client.list_namespaced_deployment(namespace)

    if deployment_name in [deployment.metadata.name for deployment in api_response.items]:
        deployed_spec = api_client.read_namespaced_deployment_status(deployment_name, namespace)
        return deployed_spec.status.conditions[0].type.upper()  # "CREATING...", "FAILED", ...
    else:
        LOG.info("Could not find a serving deployment with name '%s'" % deployment_name)

    return None


def get_deployment_name(params):
    # DNS-1123 sub-domain must consist of lower case alphanumeric characters
    regex = r'^[a-z0-9]([-a-z0-9]*[a-z0-9])?(\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*$'
    deployment_name = params["deployment_name"]
    if not re.match(regex, deployment_name):
        LOG.error("deployment name '%s' does not pass regex filter '%s'" % (deployment_name, regex))
        params["deployment_name"] = deployment_name\
            .replace("_", "-")\
            .replace(" ", "-")\
            .lower()
    return params["deployment_name"]


def get_serving_deployment_url(params, port):
    ip = params["public_ip"]
    url = "http://%s:%s" % (ip, str(port))
    return url


def get_http_method(params):
    # GET    get deployment status
    # POST   create or patch existing deployment
    # PUT    patch existing deployment
    # PATCH  patch existing deployment
    # DELETE delete deployment
    # return params.get("__ow_method", "POST").upper()  # TODO: default for local testing only, remove
    if params.get("check_status_only", False):
        return "GET"
    if params.get("delete_deployment", False):
        return "DELETE"
    return params.get("__ow_method", "POST").upper()


def run_safe(params, method):
    try:
        load_kube_config(params)
        if method in ("POST", "PATCH", "PUT"):
            LOG.info("deploying '%s' on cluster '%s'" % (params["deployment_name"], params["public_ip"]))

            spec = update_deployment_spec(params)
            deploy_result = deploy_deployment_spec(spec, params)
            service_result = deploy_service_spec(params)
            deployment_url = get_serving_deployment_url(params, service_result.spec.ports[0].node_port)
            deployment_state = get_deployment_status(params)
            result = {
                "deployment_status": deployment_state,
                "deployment_url": deployment_url
            }
        elif method == "GET":
            LOG.info("get deployment status of '%s' on cluster '%s'" % (params["deployment_name"], params["public_ip"]))
            deployment_url = get_serving_deployment_url(params)
            deployment_state = get_deployment_status(params)
            result = {
                "deployment_status": deployment_state,  # "Error"  "Creating Container"  "CrashLoopBackOff"  "Pending"
                "deployment_url": deployment_url
            }
        elif method == "DELETE":
            LOG.info("deleting deployment for '%s' on cluster '%s'" % (params["deployment_name"], params["public_ip"]))
            delete_deployment_result = delete_serving_deployment(params)
            delete_service_result = delete_serving_service(params)
            result = {
                "status": "Success"
            }
        else:
            result = {
                "status": "Failed",
                "message": "could not identify HTTP request method"
            }

        result["status"] = result.get("status", "Success")
        return result
    except Exception as e:
        LOG.exception('%s: %s' % (e.__class__.__name__, str(e)))
        return {
            "status": "Error",
            "details": {
                "error": e.__class__.__name__,
                "message": str(e),
                "trace": traceback.format_exc()
            }
        }


@app.route('/', methods=['POST'])
def deployment_api_post():
    if not request.json:
        abort(400)
    return json.dumps(run_safe(request.json,"POST"))

@app.route('/', methods=['GET'])
def deployment_api_get():
    return json.dumps(run_safe(json.loads(json.dumps(request.args)),"GET"))

@app.route('/', methods=['DELETE'])
def deployment_api_delete():
    return json.dumps(run_safe(json.loads(json.dumps(request.args)),"DELETE"))

@app.route('/', methods=['OPTIONS'])
def deployment_api_options():
    return "200"

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
