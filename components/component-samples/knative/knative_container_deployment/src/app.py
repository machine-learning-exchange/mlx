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

LOG = logging.getLogger("deploy_knative")


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


def get_knative_spec(params):
    with open("kube/knative-serving.json") as f:
        spec = json.load(f)
    return spec


def deploy_split_rule(primary_model_revision, new_revision, traffic_percentage, traffic_route_name):
    with open("kube/knative-route.json") as f:
        spec = json.load(f)

    spec["metadata"]["name"] = traffic_route_name
    name = spec["metadata"]["name"]
    namespace = "default"               # TODO: the namespace should be configured or be figured out dynamically
    plural = spec["kind"].lower()+"s"                    # TODO: verify the "rule" for constructing plural
    group, version = spec["apiVersion"].split("/")

    # Update route rule spec
    spec["spec"]["traffic"][0]["revisionName"] = primary_model_revision
    spec["spec"]["traffic"][0]["percent"] = 100 - traffic_percentage
    spec["spec"]["traffic"][1]["revisionName"] = new_revision
    spec["spec"]["traffic"][1]["percent"] = traffic_percentage

    api_client = get_custom_objects_api_client()
    api_response = api_client.list_namespaced_custom_object(group, version, namespace, plural)

    if name in [deployment["metadata"]["name"] for deployment in api_response["items"]]:
        api_response = api_client.patch_namespaced_custom_object(group, version, namespace, plural, name, spec)
    else:
        api_response = api_client.create_namespaced_custom_object(group, version, namespace, plural, spec)
    return api_response

def deploy_single_rule(revision, traffic_route_name):
    with open("kube/knative-route-single.json") as f:
        spec = json.load(f)

    spec["metadata"]["name"] = traffic_route_name
    name = spec["metadata"]["name"]
    namespace = "default"               # TODO: the namespace should be configured or be figured out dynamically
    plural = spec["kind"].lower()+"s"                    # TODO: verify the "rule" for constructing plural
    group, version = spec["apiVersion"].split("/")

    # Update route rule spec
    spec["spec"]["traffic"][0]["revisionName"] = revision

    api_client = get_custom_objects_api_client()
    api_response = api_client.list_namespaced_custom_object(group, version, namespace, plural)

    if name in [deployment["metadata"]["name"] for deployment in api_response["items"]]:
        api_response = api_client.patch_namespaced_custom_object(group, version, namespace, plural, name, spec)
    else:
        api_response = api_client.create_namespaced_custom_object(group, version, namespace, plural, spec)
    return api_response


def update_knative_spec(params):
    spec = get_knative_spec(params)

    if "container_image" in params:
        spec["spec"]["revisionTemplate"]["spec"]["container"]["image"] = params["container_image"]

    spec["metadata"]["name"] = params["deployment_name"]
    spec["spec"]["revisionTemplate"]["spec"]["container"]["ports"][0]["containerPort"] = int(params["container_port"])

    env_list = spec["spec"]["revisionTemplate"]["spec"]["container"]["env"]
    env_dict = {var["name"]: var["value"] for var in env_list}

    if "model_file_name" in params:
        env_dict["MODEL_FILE_NAME"] = params["model_file_name"]
    if "training_id" in params:
        env_dict["TRAINING_ID"] = params["training_id"]
    if "training_results_bucket" in params:
        env_dict["BUCKET_NAME"] = params["training_results_bucket"]
    if "endpoint_url" in params:
        env_dict["BUCKET_ENDPOINT_URL"] = params["endpoint_url"]
    if "access_key_id" in params:
        env_dict["BUCKET_KEY"] = params['access_key_id']
    if "secret_access_key" in params:
        env_dict["BUCKET_SECRET"] = params['secret_access_key']
    if "model_class_name" in params:
        env_dict["MODEL_CLASS_NAME"] = params['model_class_name']
    if "model_class_file" in params:
        env_dict["MODEL_CLASS_FILE"] = params['model_class_file']

    env_updated = [{"name": key, "value": value} for key, value in env_dict.items()]
    spec["spec"]["revisionTemplate"]["spec"]["container"]["env"] = env_updated

    return spec


def deploy_knative_spec(spec):
    name = spec["metadata"]["name"]
    namespace = "default"               # TODO: the namespace should be configured or be figured out dynamically
    plural = spec["kind"].lower()+"s"                    # TODO: verify the "rule" for constructing plural
    group, version = spec["apiVersion"].split("/")

    api_client = get_custom_objects_api_client()
    api_response = api_client.list_namespaced_custom_object(group, version, namespace, plural)

    if name in [deployment["metadata"]["name"] for deployment in api_response["items"]]:
        api_response = api_client.patch_namespaced_custom_object(group, version, namespace, plural, name, spec)
    else:
        api_response = api_client.create_namespaced_custom_object(group, version, namespace, plural, spec)

    # api_response_filtered = {key: api_response[key] for key in ["apiVersion", "kind"]}
    LOG.info("%s ..." % str(api_response)[:160])
    return api_response


def delete_deployment(params):
    from kubernetes.client import V1DeleteOptions

    spec = get_knative_spec(params)
    spec["metadata"]["name"] = params["deployment_name"]
    name = spec["metadata"]["name"]
    namespace = "default"               # TODO: the namespace should be configured or be figured out dynamically
    plural = spec["kind"].lower()+"s"   # TODO: verify the "rule" for constructing plural
    group, version = spec["apiVersion"].split("/")

    del_opts = V1DeleteOptions()
    api_client = get_custom_objects_api_client()
    api_response = api_client.list_namespaced_custom_object(group, version, namespace, plural)

    if name in [deployment["metadata"]["name"] for deployment in api_response["items"]]:
        api_response = api_client.delete_namespaced_custom_object(group, version, namespace, plural, name, del_opts)
    else:
        LOG.error("Could not find the knative serving deployment '%s'" % name)
        return {
            "status": "Error",
            "details": "Could not find a knative serving deployment with name '%s'" % name
        }

    # api_response_filtered = {key: api_response[key] for key in ["apiVersion", "kind"]}
    LOG.info("%s ..." % str(api_response)[:160])
    return api_response


def get_service_name(params):
    # 'knative_DEPLOYMENT_ID': 'fashion-mnist'
    # 'PREDICTOR_ID':         'single-model'
    # 'PREDICTIVE_UNIT_ID':   'classifier'
    knative_spec = get_knative_spec(params)
    spec_name = get_deployment_name(params)  # knative_spec["spec"]["name"])  # 'fashion-mnist'
    predictor_name = knative_spec["spec"]["predictors"][0]["name"]  # 'single-model'
    graph_name = knative_spec["spec"]["predictors"][0]["graph"]["name"]  # 'classifier' (== containers[0].name)
    pod_name_prefix = "%s-%s-%s" % (spec_name, predictor_name, graph_name)
    return pod_name_prefix  # 'fashion-mnist-single-model-classifier'


def get_pods(params):
    api_client_v1 = get_api_client_v1()
    pods = api_client_v1.list_namespaced_pod(namespace="default", watch=False)
    pod_name_prefix = get_service_name(params)  # 'fashion-mnist-single-model-classifier'
    deployment_name = get_deployment_name(params)
    training_id = params["training_id"]

    def match_knative_deployment(pod):
        if not pod.metadata.name.startswith(pod_name_prefix):
            return False
        env = {var.name: var.value for var in pod.spec.containers[0].env}
        return env["knative_DEPLOYMENT_ID"] == deployment_name and \
               env["TRAINING_ID"] == training_id

    return list(filter(match_knative_deployment, pods.items))


def get_deployment_status(params):
    # AVAILABLE (classifier URL actually available)
    # READY (pod status, not url availability)
    # UNKNOWN (no pods)
    # ERROR (CrashLoopBackOff, Succeeded - if pod terminated, will not be restarted, this should not happen)
    # PENDING (Creating..., ContainerCreating, ContainersReady, PodScheduled, Pending, Initialized, Running)
    pods = get_pods(params)
    if not pods:
        status = get_deployment_state(params) or "Unknown"
    else:
        status_conditions = sorted(pods[0].status.conditions, key=lambda status: status.last_transition_time, reverse=True)
        status = status_conditions[0].type

    if status in ["Creating...", "ContainerCreating", "ContainersReady", "PodScheduled", "Initialized", "Running"]:
        status = "Pending"

    if status in ["CrashLoopBackOff", "Unschedulable", "Failed", "Succeeded"]:
        status = "Error"

    if status == "Ready":
        status = "Available"

    return status.upper()


def get_deployment_state(params):
    deployment_name = get_deployment_name(params)
    spec = get_knative_spec(params)
    group, version = spec["apiVersion"].split("/")
    namespace = "default"                # TODO: the namespace should be configured or be figured out dynamically
    plural = spec["kind"].lower() + "s"  # TODO: verify the "rule" for constructing plural
    api_client = get_custom_objects_api_client()
    api_response = api_client.list_namespaced_custom_object(group, version, namespace, plural)

    if deployment_name in [deployment["metadata"]["name"] for deployment in api_response["items"]]:
        deployed_spec = api_client.get_namespaced_custom_object(group, version, namespace, plural, deployment_name)
        env_list = deployed_spec["spec"]["predictors"][0]["componentSpecs"][0]["spec"]["containers"][0]["env"]
        env_dict = {var["name"]: var["value"] for var in env_list}
        deployed_training_id = env_dict["TRAINING_ID"]
        if params["training_id"] == deployed_training_id and "status" in deployed_spec:
            return deployed_spec["status"]["state"].upper()  # "CREATING...", "FAILED", ...
    else:
        LOG.info("Could not find a knative serving deployment with name '%s'" % deployment_name)

    return None


def get_ambassador_port():
    from kubernetes.client.rest import ApiException
    api_client_v1 = get_api_client_v1()
    try:
        svc = api_client_v1.read_namespaced_service(namespace="default", name="knative-core-ambassador")
    except ApiException:
        svc = api_client_v1.read_namespaced_service(namespace="default", name="ambassador")
    port = svc.spec.ports[0].node_port
    return port


def get_deployment_name(params):
    # DNS-1123 sub-domain must consist of lower case alphanumeric characters (or knative will raise an exception)
    regex = r'^[a-z0-9]([-a-z0-9]*[a-z0-9])?(\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*$'
    deployment_name = params["deployment_name"]
    if not re.match(regex, deployment_name):
        LOG.error("deployment name '%s' does not pass knative regex filter '%s'" % (deployment_name, regex))
        params["deployment_name"] = deployment_name\
            .replace("_", "-")\
            .replace(" ", "-")\
            .lower()
    return params["deployment_name"]


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
        # method = get_http_method(params)
        if method in ("POST", "PATCH", "PUT"):
            # if set(deployment_parameters).issubset(params.keys()):
            LOG.info("deploying '%s'" % (params["deployment_name"]))
            spec = update_knative_spec(params)
            deploy_result = deploy_knative_spec(spec)
            print(deploy_result)
            revision_name = deploy_result.get("status", "first")
            if revision_name == "first":
                revision_name = (params["deployment_name"] + "-00001")
            else:
                breakdown_names = revision_name["latestCreatedRevisionName"].split("-")
                version = breakdown_names[-1]
                version = int(version) + 1
                revision_name = (params["deployment_name"] + ("-%05d" % version))
            result = {
                "deployment_status": "deployed",
                "deployment_revision": revision_name,
                "details": deploy_result
            }
        elif method == "GET":
            result = {
                "deployment_status": "UNKNOWN"  # "Error"  "Creating Container"  "CrashLoopBackOff"  "Pending"
            }
        elif method == "DELETE":
            LOG.info("deleting deployment for '%s'" % (params["deployment_name"]))
            delete_result = delete_deployment(params)
            result = {
                "status": delete_result["status"],
                "details": delete_result["details"]
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
    return json.dumps(run_safe(request.json, "POST"))


@app.route('/route-rule', methods=['POST'])
def rule_api_post():
    if not request.json:
        abort(400)
    return json.dumps(deploy_split_rule(request.json['primary_model_revision'], request.json['deployment_revision'], request.json['traffic_percentage'], request.json['traffic_route_name']))


@app.route('/route-single-rule', methods=['POST'])
def single_rule_api_post():
    if not request.json:
        abort(400)
    return json.dumps(deploy_single_rule(request.json['revision'], request.json['traffic_route_name']))


@app.route('/', methods=['GET'])
def deployment_api_get():
    return json.dumps(run_safe(json.loads(json.dumps(request.args)), "GET"))


@app.route('/', methods=['DELETE'])
def deployment_api_delete():
    return json.dumps(run_safe(json.loads(json.dumps(request.args)),"DELETE"))


@app.route('/', methods=['OPTIONS'])
def deployment_api_options():
    return "200"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
