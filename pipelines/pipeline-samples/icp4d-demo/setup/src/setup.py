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


def createSecret(secret_list, secret_name):
    try:
        delete_command = ['./kubectl', 'delete', 'secret', secret_name]
        subprocess.run(delete_command, check=True)
    except Exception as e:
        print('No previous secret: ' + secret_name + '. Secret deletion is not performed.')
    command = ['./kubectl', 'create', 'secret', 'generic', secret_name]
    for arg in secret_list:
        command.append(arg)
    subprocess.run(command, check=True)
    subprocess.run(['./kubectl', 'describe', 'secret', secret_name], check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--secret_name', type=str, help='Credential secret name', default="sklearn-creds")
    args = parser.parse_args()

    secret_name = args.secret_name

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

    res= requests.post('https://iam.test.cloud.ibm.com/identity/token', data=payload, headers=headers)
    token = json.loads(res.text)['access_token']

    # Get Connection ID
    headers={
        'Authorization': 'Bearer ' + token
    }
    res = requests.get('https://api.dataplatform.dev.cloud.ibm.com/v2/data_assets/'  + data_assets + '?project_id=' + project_id, headers=headers)
    connection_id = json.loads(res.text)['attachments'][0]['connection_id']

    # Get creds
    headers={
        'Authorization': 'Bearer ' + token
    }
    res = requests.get('https://api.dataplatform.dev.cloud.ibm.com/v2/connections/' + connection_id + '?project_id=' + project_id, headers=headers)
    creds = json.loads(res.text)['entity']['properties']

        # Create Postgres URL
    postgres_url = 'postgresql://' + str(creds['username']) + ':' + str(creds['password']) + '@' + str(creds['host']) + ':' + str(creds['port']) + '/' + str(creds['database'])

    secret_list = []
    secret_list.append('--from-literal=%s=\'%s\'' % ('POSTGRES_URL', postgres_url))
    # Generate secret for the pipeline
    if secret_list:
        get_kubectl()
        createSecret(secret_list, secret_name)
