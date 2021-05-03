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
import requests
import random
import string

from app import run_safe, deploy_split_rule, deploy_single_rule

def get_secret(path):
    with open(path, 'r') as f:
        cred = f.readline().strip('\'')
    f.close()
    return cred

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_id', type=str, help='Training model id', default="training-dummy")
    parser.add_argument('--metric_path', type=str, help='Path for deployment output', default="/tmp/log.txt")
    parser.add_argument('--cleanup', type=bool, help='Cleanup previous model deployments', default=False)
    parser.add_argument('--traffic_percentage', type=int, help='percentage of traffic that route to the new version of the model', default=5)
    parser.add_argument('--primary_model_revision', type=str, help='primary revision model', default="model-serving-00001")
    parser.add_argument('--traffic_route_name', type=str, help='name for knative service route rule', default="knative-demo")
    parser.add_argument('--model_serving_image', type=str, help='Model serving container image', default="tomcli/knative-serving:pytorch")
    parser.add_argument('--model_class_name', type=str, help='PyTorch model class name', default='ModelClass')
    parser.add_argument('--model_class_file', type=str, help='File that contains the PyTorch model class', default='model_class.py')
    parser.add_argument('--deployment_name', type=str, help='Model Deployment Name', default='model-serving')
    parser.add_argument('--container_port', type=int, help='Application port number of the model container', default=5000)
    parser.add_argument('--model_file_name', type=str, help='Model binary filename', default='model.pt')
    parser.add_argument('--namespace', type=str, help='Kubernetes namespace to deploy the model', default='default')

    args = parser.parse_args()

    metric_path = args.metric_path
    model_id = args.model_id
    cleanup = args.cleanup
    traffic_percentage = args.traffic_percentage
    primary_model_revision = args.primary_model_revision
    traffic_route_name = args.traffic_route_name
    model_serving_image = args.model_serving_image
    model_class_name = args.model_class_name
    model_class_file = args.model_class_file
    deployment_name = args.deployment_name
    container_port = args.container_port
    model_file_name = args.model_file_name
    namespace = args.namespace

    s3_url = get_secret("/app/secrets/s3_url")
    bucket_name = get_secret("/app/secrets/result_bucket")
    s3_username = get_secret("/app/secrets/s3_access_key_id")
    s3_password = get_secret("/app/secrets/s3_secret_access_key")
    kiali_domain_name = get_secret("/app/secrets/kiali_domain_name")
    knative_ingress = get_secret("/app/secrets/knative_ingress")

    try:
        local_cluster_deployment = str(get_secret("/app/secrets/local_cluster_deployment").lower()) == 'true'
    except Exception as e:
        local_cluster_deployment = False

    try:
        knative_custom_domain = get_secret("/app/secrets/knative_custom_domain")
    except Exception as e:
        knative_custom_domain = 'example.com'

    if local_cluster_deployment:
        knative_url = None
    else:
        knative_url = get_secret("/app/secrets/knative_url")

    # Model Deployment parameters
    formData = {
        "endpoint_url": s3_url,
        "access_key_id": s3_username,
        "secret_access_key": s3_password,
        "training_results_bucket": bucket_name,
        "model_file_name": model_file_name,
        "deployment_name": deployment_name,
        "training_id": model_id,
        "container_image": model_serving_image,
        "check_status_only": False,
        "model_class_name": model_class_name,
        "model_class_file": model_class_file,
        "container_port": container_port,
        "namespace": namespace,
        "submission_id": "".join([random.choice(string.ascii_letters) for i in range(6)])
    }

    # Deploy model with Knative route.
    if cleanup:
        if local_cluster_deployment:
            # Using K8s api
            metrics = run_safe(formData, "DELETE")
        else:
            response = requests.delete(knative_url, params=formData)
            metrics = response.json()
        print("Successfully cleanup old deployments")
    else:
        if local_cluster_deployment:
            # Using K8s api
            metrics = run_safe(formData, "POST")
        else:
            response = requests.post(knative_url, json=formData)
            metrics = response.json()
        rule_output = ""
        if metrics['deployment_revision'] != (deployment_name + '-00001'):
            if traffic_percentage < 0:
                print('The Traffic for the new model can not be less than 0.')
                exit(1)
            formData_split = {
                'primary_model_revision': primary_model_revision,
                'deployment_revision': metrics['deployment_revision'],
                'traffic_percentage': traffic_percentage,
                'traffic_route_name': traffic_route_name,
                'namespace': namespace
            }
            if local_cluster_deployment:
                # Using K8s api
                deploy_split_rule(formData_split['primary_model_revision'], formData_split['deployment_revision'], formData_split['traffic_percentage'], formData_split['traffic_route_name'], formData_split['namespace'])
            else:
                res = requests.post(knative_url + '/route-rule', json=formData_split)
                rule_output = res.json()
            print("Traffic split to " + str(100-traffic_percentage) + ":" + str(traffic_percentage) + ".\n")
        else:
            formData_split = {
                'revision': deployment_name + '-00001',
                'traffic_route_name': traffic_route_name,
                'namespace': namespace
            }
            if local_cluster_deployment:
                # Using K8s api
                deploy_single_rule(formData_split['revision'], formData_split['traffic_route_name'], formData_split['namespace'])
            else:
                res = requests.post(knative_url + '/route-single-rule', json=formData_split)
                rule_output = res.json()

        # Print out the necessary endpoints and debugging outputs.
        metrics['Prediction_Host'] = traffic_route_name + "." + namespace + "." + knative_custom_domain
        metrics['Prediction_Endpoint'] = knative_ingress
        metrics['kiali_Link'] = "http://" + kiali_domain_name + "/console/graph/namespaces/?edges=requestsPercentOfTotal&graphType=versionedApp&namespaces=" + namespace + "&injectServiceNodes=true&duration=60&pi=5000&layout=dagre"

        # print("Debugging outputs:")
        # print(metrics)
        metrics.pop('details', None)

        print("\n\nEndpoint IP for these models: " + metrics['Prediction_Endpoint'] + " . Model prediction host is " + metrics['Prediction_Host'])
        print("Kiali link: http://" + kiali_domain_name + "/console/graph/namespaces/?edges=requestsPercentOfTotal&graphType=versionedApp&namespaces=" + namespace + "&injectServiceNodes=true&duration=60&pi=5000&layout=dagre")

    with open(metric_path, "w") as report:
        report.write(json.dumps(metrics))
