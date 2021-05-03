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

from app import run_safe

def get_secret(path):
    with open(path, 'r') as f:
        cred = f.readline().strip('\'')
    f.close()
    return cred

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--metric_path', type=str, help='Path for deployment output', default="/tmp/log.txt")
    parser.add_argument('--cleanup', type=bool, help='Cleanup previous model deployments', default=False)
    parser.add_argument('--model_serving_image', type=str, help='Model serving container image', default="tomcli/knative-serving:pytorch")
    parser.add_argument('--deployment_name', type=str, help='Model Deployment Name', default='model-serving')
    parser.add_argument('--container_port', type=int, help='Application port number of the model container', default=5000)
    args = parser.parse_args()

    metric_path = args.metric_path
    cleanup = args.cleanup
    model_serving_image = args.model_serving_image
    deployment_name = args.deployment_name
    container_port = args.container_port

    public_ip = get_secret("/app/secrets/public_ip")

    try:
        local_cluster_deployment = str(get_secret("/app/secrets/local_cluster_deployment").lower()) == 'true'
    except Exception as e:
        local_cluster_deployment = False

    if local_cluster_deployment:
        k8s_controller_url = None
    else:
        k8s_controller_url = get_secret("/app/secrets/k8s_controller_url")

    formData = {
        "public_ip": public_ip,
        "deployment_name": deployment_name,
        "container_port": container_port,
        "container_image": model_serving_image,
        "check_status_only": False
    }

    if cleanup:
        if local_cluster_deployment:
            metrics = run_safe(formData, "DELETE")
        else:
            response = requests.delete(k8s_controller_url, params=formData)
            metrics = response.json()
    else:
        if local_cluster_deployment:
            metrics = run_safe(formData, "POST")
        else:
            response = requests.post(k8s_controller_url, json=formData)
            metrics = response.json()
        print(metrics)

    with open(metric_path, "w") as report:
        report.write(json.dumps(metrics))
