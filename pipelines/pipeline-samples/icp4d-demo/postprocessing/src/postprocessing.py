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
import subprocess
import os
import configparser

def get_secret_creds(path):
    with open(path, 'r') as f:
        cred = f.readline().strip('\'')
    f.close()
    return cred

def get_kubectl():
    res = requests.get('https://storage.googleapis.com/kubernetes-release/release/v1.14.0/bin/linux/amd64/kubectl', allow_redirects=True)
    open('kubectl', 'wb').write(res.content)
    subprocess.call(['chmod', '755', 'kubectl'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_id', type=str, help='trained model id', default="maintenance-model")
    parser.add_argument('--notification_type', type=str, help='Notification type', default="training")
    parser.add_argument('--pipeline_name', type=str, help='name of the pipeline', default="pipeine_name")
    parser.add_argument('--serving_output', type=str, help='Serving output details', default="{}")
    parser.add_argument('--notification', type=str, help='Send notification to cp4d platform', default="true")
    args = parser.parse_args()

    model_id = args.model_id
    notification_type = args.notification_type.lower()
    pipeline_name = args.pipeline_name
    notification = args.notification.lower()
    serving_output = json.loads(args.serving_output)

    if notification == 'true':
        project_id = get_secret_creds("/app/secrets/project_id")
        api_key = get_secret_creds("/app/secrets/api_key")
        data_assets = get_secret_creds("/app/secrets/data_assets")

        # Get bearer token
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        payload = {
            'grant_type': 'urn:ibm:params:oauth:grant-type:apikey',
            'response_type': 'cloud_iam',
            'apikey': api_key
        }

        res = requests.post('https://iam.test.cloud.ibm.com/identity/token', data=payload, headers=headers)
        token = json.loads(res.text)['access_token']
    else:
        project_id = ""
        api_key = ""
        data_assets = ""
        token = ""
    model_revision = ""
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + token
    }
    if notification_type == 'training':
        if notification == 'true':
            headers = {
                'Authorization': 'Bearer ' + token
            }
            model_payload = {
                "project_id": project_id,
                "name": "Trained KFP model",
                "description": "An example of an asset created from KFP pipeline after training a model",
                "model_id": model_id
            }

            res = requests.post('https://dataplatform.dev.cloud.ibm.com/api/os/kfp-model', data=model_payload, headers=headers)
            try:
                print(res.json())
            except:
                print("Model Status update Failed. Please check your credentials.")
        else:
            print("Model training is completed. The model is registered at http://169.45.69.227:30541/os/models/maintenance-model")
    elif notification_type == 'serving':
        public_ip = get_secret_creds("/app/ip/public_ip")
        get_kubectl()
        result = subprocess.run(['bash', '-c', './kubectl get svc -n istio-system kiali -o jsonpath="{.spec.ports[0].nodePort}"'], stdout=subprocess.PIPE)
        port = str(result.stdout).replace('b', '').replace("'","")
        if port != '':
            if notification == 'true':
                print('Monitoring Dashboard: https://dataplatform.dev.cloud.ibm.com/os/analyze-kiali?context=os\n')
            print('Monitoring Dashboard: http://' + public_ip + ':' + port + '/kiali\n \n')
            try:
                model_revision = serving_output['status']['default']['predictor']['name']
                namespace = serving_output['metadata']['namespace']
                print("Model Revision: " + model_revision + "\n \n")
                if notification == 'true':
                    print('Metric Board for this model: https://dataplatform.dev.cloud.ibm.com/os/analyze-kiali/console/namespaces/' + namespace + '/services/' + model_revision + '?tab=metrics&duration=1800&reporter=source&context=os \n')
                    print('Kiosk Metric Board for this model: https://dataplatform.dev.cloud.ibm.com/os/analyze-kiali/console/namespaces/' + namespace + '/services/' + model_revision + '?tab=metrics&duration=1800&reporter=source&context=os&kiosk=true \n')
                else:
                    print('Kiosk Metric Board for this model: http://' + public_ip + ':' + port + '/kiali/console/namespaces/' + namespace + '/services/' + model_revision + '?tab=metrics&duration=1800&reporter=source&kiosk=true \n')
                print('Metric Board for this model: http://' + public_ip + ':' + port + '/kiali/console/namespaces/' + namespace + '/services/' + model_revision + '?tab=metrics&duration=1800&reporter=source \n \n')
                if notification == 'true':
                    print('Traffic Graph for this model: https://dataplatform.dev.cloud.ibm.com/os/analyze-kiali/console/graph/namespaces/?edges=requestsPercentage&graphType=service&injectServiceNodes=true&duration=1800&pi=10000&namespaces=' + namespace + '&layout=dagre&context=os \n')
                    print('Kiosk Traffic Graph for this model: https://dataplatform.dev.cloud.ibm.com/os/analyze-kiali/console/graph/namespaces/?edges=requestsPercentage&graphType=service&injectServiceNodes=true&duration=1800&pi=10000&namespaces=' + namespace + '&layout=dagre&context=os&kiosk=true \n')
                else:
                    print('Kiosk Traffic Graph for this model: http://' + public_ip + ':' + port + '/kiali/console/graph/namespaces/?edges=requestsPercentage&graphType=service&injectServiceNodes=true&duration=1800&pi=10000&namespaces=' + namespace + '&layout=dagre&kiosk=true \n')
                print('Traffic Graph for this model: http://' + public_ip + ':' + port + '/kiali/console/graph/namespaces/?edges=requestsPercentage&graphType=service&injectServiceNodes=true&duration=1800&pi=10000&namespaces=' + namespace + '&layout=dagre \n \n')
            except:
                pass
        else:
            print('Kiali Dashboard is not expose to the public.\n')
        if notification == 'true':
            message = "Kubeflow Pipeline - Model is now served."
            payload = {
                "content": message,
                "type": "Announce",
                "actor": {
                    "type": "Service",
                    "name": "Kubeflow Pipeline",
                    "id": "http://dataplatform.ibm.com/alert-succeeded"
                },
                "target": {
                    "name": "PROJECT NAME",
                    "type": "https://dataplatform.ibm.com/Project",
                    "url": "/projects/" + project_id + "?context=os",
                    "id": "https://api.dataplatform.dev.cloud.ibm.com/v2/projects/" + project_id
                },
                "generator": {
                    "type": "Service",
                    "name": "Kubeflow Pipeline"
                }
            }
            res = requests.post('https://api.dataplatform.dev.cloud.ibm.com/v1/notifications', json=payload, headers=headers)
            try:
                print("Notification Status:")
                print(res)
                print("Notification Message: " + message)
            except:
                print("Model Status update Failed. Please check your credentials.")
    else:
        if notification_type == 'etl':
            message = "Kubeflow Pipeline - ETL Pipeline Completed."
        else:
            message = "Kubeflow Pipeline - Scoring and Monitoring clients provisioned."
        payload = {
            "content": message,
            "type": "Announce",
            "actor": {
                "type": "Service",
                "name": "Kubeflow Pipeline",
                "id": "http://dataplatform.ibm.com/alert-succeeded"
            },
            "target": {
                "name": "PROJECT NAME",
                "type": "https://dataplatform.ibm.com/Project",
                "url": "/projects/" + project_id + "?context=os",
                "id": "https://api.dataplatform.dev.cloud.ibm.com/v2/projects/" + project_id
            },
            "generator": {
                "type": "Service",
                "name": "Kubeflow Pipeline"
            }
        }
        res = requests.post('https://api.dataplatform.dev.cloud.ibm.com/v1/notifications', json=payload, headers=headers)
        try:
            print("Notification Status:")
            print(res)
            print("Notification Message: " + message)
        except:
            print("Model Status update Failed. Please check your credentials.")
    if not os.path.exists(os.path.dirname('/tmp/model-revision')):
        os.makedirs(os.path.dirname('/tmp/model-revision'))
    with open('/tmp/model-revision', "w") as report:
        report.write(json.dumps({"model-revision": model_revision}))
