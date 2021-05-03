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
import requests
import json
import argparse
import re


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_url', type=str, help='Serving URL for the gender classification model')
    parser.add_argument('--knative_host', type=str, help='Host for the gender classification model', default='')
    parser.add_argument('--loop', type=bool, help='Produce traffic with forever loop', default=False)
    args = parser.parse_args()

    url = re.compile(r"https?://")

    if args.knative_host:
        headers = {
            'Host': args.knative_host
        }
    else:
        headers = {}
    request = {"timestamp": "2019-09-04 T15:31 Z",
               "containerID": "C100",
               "temperature": 5.49647,
               "target_temperature": 6.0,
               "ambiant_temperature": 19.8447,
               "kilowatts": 3.44686,
               "content_type": 2,
               "oxygen_level": 20.4543,
               "nitrogen_level": 79.4046,
               "carbon_dioxide_level": 4.42579,
               "humidity_level": 60.3148,
               "vent_1": "True",
               "vent_2": "True",
               "vent_3": "True",
               "time_door_open": 0.822024,
               "defrost_cycle": 6
               }

    response = requests.post('http://' + args.model_url, json=request, headers=headers)
    print(response)
    try:
        print("Prediction Class: [maintenance]")
        print(response.text)

        while args.loop:
            response = requests.post('http://' + args.model_url, json=request, headers=headers)
            print(response.text)
    except:
        print("Model is not ready, please try again")
