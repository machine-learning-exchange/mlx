#!/usr/bin/env python3

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


import connexion

from flask_cors import CORS
from swagger_server import encoder
from swagger_server import VERSION


def main():

    print(" * MLX API version: %s" % VERSION)

    cx_app = connexion.App(__name__, specification_dir='./swagger/')

    flask_app = cx_app.app
    flask_app.json_encoder = encoder.JSONEncoder

    print(" * Enabled cross-origin support with 'flask-cors': origins='*'")
    CORS(flask_app, origins='*')

    cx_app.add_api('swagger.yaml', arguments={'title': 'MLX API'})

    cx_app.run(port=8080)


if __name__ == '__main__':
    main()
