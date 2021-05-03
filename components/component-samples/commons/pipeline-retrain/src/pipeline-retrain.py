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
import sys
import requests
import random
import string
import json
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--parameters', type=str, help='Pipeline Parameters', default="{'parameters':[]}")
    parser.add_argument('--pipeline_url', type=str, help='KubeFlow pipeline URL', default="http://xxx.xx.xxx.xx/pipeline")
    parser.add_argument('--pipeline_id', type=str, help='Retraining Pipeline ID', default="dummy-id")
    parser.add_argument('--experiment_id', type=str, help='Retraining experiment ID', default="dummy-id")
    parser.add_argument('--model_id', type=str, help='Original model ID', default="training-xxx")
    args = parser.parse_args()

    parameters = args.parameters
    pipeline_url = args.pipeline_url
    pipeline_id = args.pipeline_id
    experiment_id = args.experiment_id
    model_id = args.model_id
    print(parameters)
    param = json.loads(parameters)

    pipelineURL = pipeline_url + '/apis/v1beta1/runs'
    rand_id = "".join([random.choice(string.ascii_letters) for i in range(6)])
    name = "retrain-pipeline-" + rand_id
    payload={"description":"",
              "name": name,
              "pipeline_spec":
                  {"parameters": param["parameters"],
                   "pipeline_id": pipeline_id},
                   "resource_references": [{"key":
                                           {"id": experiment_id,
                                            "type":"EXPERIMENT"},
                                            "relationship":"OWNER"}]}
    response = requests.post(pipelineURL, json=payload)
    print(response.json())
    print('The model ' + model_id + ' was unsatisfied for deployment. Thus, a new pipeline run ' + name + ' has been submitted.')

    with open('/tmp/logs.txt', "w") as report:
        report.write('Retrain Pipeline name is ' + name)
