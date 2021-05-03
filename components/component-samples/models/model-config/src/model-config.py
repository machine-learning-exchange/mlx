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
from ruamel.yaml import YAML
import subprocess
import os
import configparser

yaml = YAML(typ='safe')


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


def get_kubectl():
    res = requests.get('https://storage.googleapis.com/kubernetes-release/release/v1.14.0/bin/linux/amd64/kubectl', allow_redirects=True)
    open('kubectl', 'wb').write(res.content)
    subprocess.call(['chmod', '755', 'kubectl'])


def get_secret_creds(path):
    with open(path, 'r') as f:
        cred = f.readline().strip('\'')
    f.close()
    return cred


def loadModelFile(model_id):
    model_api = 'mlx-api'  # Pull KubeDNS address from secret in the future
    model_url = 'http://' + model_api + '/apis/v1alpha1/models/' + model_id + '/templates'
    response = requests.get(model_url)
    metrics = response.json()
    data = yaml.load(metrics['template'])
    return data


def writeFile(path, content):
    with open(path, "w") as report:
        report.write(content)


def generateFfdlParams(model_dict, param_path, creds):
    ffdl_params = {
        'model_def_file_path': '',
        'manifest_file_path': '',
        'training_job_name': '',
        'training_job_description': '',
        'training_job_version': '',
        'training_job_gpus': '',
        'training_job_cpus': '',
        'training_job_learners': '',
        'training_job_memory': '',
        'training_job_framework_name': '',
        'training_job_framework_version': '',
        'training_job_command': '',
        'training_job_metric_type': '',
        'training_job_metric_path': ''
    }

    ffdl_secret_params = {
        's3_url': '',
        'training_bucket': '',
        'result_bucket': '',
        's3_access_key_id': '',
        's3_secret_access_key': '',
        'ffdl_rest': ''
    }

    for key, value in ffdl_params.items():
        writeFile(param_path + key, value)


def generateWmlParams(model_dict, param_path, secret_list, creds):
    wml_params = {
        'train_code': model_dict['train']['model_source']['initial_model']['path'],
        'execution_command': model_dict['train']['execution']['command'],
        'config': 'created_secret',
        'framework': model_dict['framework']['name'],
        'framework_version': model_dict['framework']['version'],
        'runtime': model_dict['framework']['runtimes']['name'],
        'runtime_version': model_dict['framework']['runtimes']['version'],
        'run_definition': model_dict['name'].replace(' ', '-') + '-definition',
        'run_name': model_dict['name'].replace(' ', '-') + '-run',
        'author_email': model_dict['author']['email']
    }

    wml_secret_params = {
        'wml_url': creds['wml_url'],
        'wml_apikey': creds['wml_apikey'],
        'wml_instance_id': creds['wml_instance_id'],
        'wml_data_source_type': model_dict['data_stores'][0]['type'],
        'cos_endpoint': model_dict['data_stores'][0]['connection']['endpoint'],
        'cos_access_key': creds['cos_access_key'],
        'cos_secret_key': creds['cos_secret_key'],
        'cos_input_bucket': model_dict['train']['data_source']['training_data']['bucket'],
        'cos_output_bucket': model_dict['train']['model_training_results']['trained_model']['bucket']
    }

    for key, value in wml_params.items():
        writeFile(param_path + key, value)

    for key in wml_secret_params:
        secret_list.append('--from-literal=%s=\'%s\'' % (key, wml_secret_params[key]))

def generateKnativeDeployParams(model_dict, param_path):
    knative_params = {
        'model_serving_image': model_dict['serve']['serving_container_image']['container_image_url'],
        'deployment_name': model_dict['model_identifier'],
        'model_class_name': '',
        'model_class_file': '',
        'container_port': '5000',
        'traffic_route_name': 'knative-demo',
        'primary_model_revision': model_dict['model_identifier'] + '-00001',
        'traffic_percentage': '5'
    }

    knative_secret_params = {
        's3_url': model_dict['data_stores'][0]['connection']['endpoint'] if 'data_stores' in model_dict else '',
        'result_bucket': '',
        's3_access_key_id': '',
        's3_secret_access_key': '',
        'kiali_domain_name': '',
        'knative_url': '',
        'knative_custom_domain': ''
    }

    for key, value in knative_params.items():
        writeFile(param_path + key, value)


def generateKFServingDeployParams(model_dict, param_path):
    kfserving_params = {
        'model_serving_image': model_dict['serve']['serving_container_image']['container_image_url'],
        'deployment_name': model_dict['model_identifier'],
        'container_port': '5000',
        'default_custom_model_spec': json.dumps({"name": model_dict['model_identifier'],
                                      "image": model_dict['serve']['serving_container_image']['container_image_url'],
                                      "port": "5000"})
    }

    for key, value in kfserving_params.items():
        writeFile(param_path + key, value)

def generateKubeDeployParams(model_dict, param_path):
    kube_params = {
        'model_serving_image': model_dict['serve']['serving_container_image']['container_image_url'],
        'deployment_name': model_dict['model_identifier'],
        'model_class_name': '',
        'model_class_file': '',
        'container_port': '5000',
        'traffic_route_name': 'knative-demo',
    }

    kube_secret_params = {
        's3_url': model_dict['data_stores'][0]['connection']['endpoint'] if 'data_stores' in model_dict else '',
        'result_bucket': '',
        's3_access_key_id': '',
        's3_secret_access_key': '',
        'kube_controller_url': ''
    }

    for key, value in kube_params.items():
        writeFile(param_path + key, value)


def get_github_creds(github_token, github_url):
    config_file = os.path.basename(github_url)
    config_local_path = os.path.join('/tmp', config_file)
    command = ['curl', '-H', 'Authorization: token %s' % github_token, '-L', '-o', config_local_path, github_url]
    subprocess.run(command, check=True)
    config = configparser.ConfigParser()
    config.read(config_local_path)
    creds = {}
    for section in config.sections():
        for key in config[section]:
            creds[key] = config[section][key]
    return creds


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_id', type=str, help='Model id', default="max-image-caption-generator")
    parser.add_argument('--secret_name', type=str, help='Secret name to store the model credentials', default="model-secret")
    parser.add_argument('--param_path', type=str, help='Path to store each parameters', default="/tmp/")
    parser.add_argument('--github_token', type=str, help='GitHub Token to access the private repository', default="")
    parser.add_argument('--github_url', type=str, help='GitHub URL that has the credentials in INI format', default="")

    args = parser.parse_args()

    model_id = args.model_id
    secret_name = args.secret_name
    param_path = args.param_path
    github_token = args.github_token
    github_url = args.github_url

    model_dict = loadModelFile(model_id)
    secret_list = []

    # Training params
    if 'train' in model_dict and model_dict['train']['trainable']:
        if str(model_dict['train'].get('credentials_required', 'false')).lower() == 'true':
            creds = get_github_creds(github_token, github_url)
        else:
            creds = {}
            print("Credentials file is required for training.")
            exit(1)
        for item in model_dict['train']['tested_platforms']:
            if item.lower() == 'watsonml':
                generateWmlParams(model_dict, param_path, secret_list, creds)
            if item.lower() == 'ffdl':
                generateFfdlParams(model_dict, param_path, creds)

    # Serving params
    if 'serve' in model_dict and model_dict['serve']['servable']:
        if 'train' in model_dict and str(model_dict['train'].get('credentials_required', 'false')).lower() == 'true':
            creds = get_github_creds(github_token, github_url)
        else:
            creds = {}
        for item in model_dict['serve']['tested_platforms']:
            if item.lower() == 'knative':
                generateKnativeDeployParams(model_dict, param_path)
            if item.lower() == 'kubernetes':
                generateKubeDeployParams(model_dict, param_path)
            if item.lower() == 'kfserving' or True:
                generateKFServingDeployParams(model_dict, param_path)

    # Generate secret for the pipeline
    if secret_list:
        get_kubectl()
        createSecret(secret_list, secret_name)
    
    print('done')
