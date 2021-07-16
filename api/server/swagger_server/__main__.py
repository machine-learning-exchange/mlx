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
import logging

from datetime import datetime
from flask import redirect, request
from flask_cors import CORS
from os import environ as env
from swagger_server import encoder
from swagger_server import VERSION
from waitress import serve
from threading import current_thread


def main():

    logging.basicConfig(format="%(asctime)s.%(msecs)03d %(levelname)-7s [%(name)-.8s] %(message)s",
                        datefmt="%Y/%m/%d %H:%M:%S",
                        level=env.get("LOGLEVEL", logging.INFO))

    log = logging.getLogger("flaskapp")

    log.info("MLX API version: %s" % VERSION)

    cx_app = connexion.App(__name__, specification_dir='./swagger/')
    cx_app.add_api('swagger.yaml', arguments={'title': 'MLX API'})

    flask_app = cx_app.app
    flask_app.json_encoder = encoder.JSONEncoder

    log.info("Enable cross-origin support with 'flask-cors': origins='*'")
    CORS(flask_app, origins='*')

    start_times = dict()

    def get_request_log_msg():
        return '(%03d) %s %s %s ...' % (current_thread().ident % 1000, request.remote_addr,
                                        request.method, request.full_path)

    @flask_app.before_request
    def before_request():
        msg = get_request_log_msg()
        log.info(msg)
        start_times[msg] = datetime.now()

    @flask_app.after_request
    def after_request(response):
        msg = get_request_log_msg()
        time_delta = datetime.now() - start_times.pop(msg)
        elapsed_millis = time_delta.seconds * 1000 + time_delta.microseconds / 1000
        outstanding_requests = len(start_times)
        log_func = get_log_method_by_response_status(response)
        log_func('%s %s (%i ms) [%i]', msg, response.status, elapsed_millis, outstanding_requests)
        return response

    log_functions = [log.info, log.info, log.info, log.info, log.warning, log.error]

    def get_log_method_by_response_status(response):
        log_level_idx = response.status_code // 100
        log_func = log_functions[log_level_idx]
        return log_func

    @flask_app.route("/")
    def index():
        return redirect("/apis/v1alpha1/ui/#!/", code=302)

    # cx_app.run(port=8080)
    serve(flask_app, host="0.0.0.0", port=8080, threads=32)


if __name__ == '__main__':
    main()
