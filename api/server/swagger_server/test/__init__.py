# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0
import logging

import connexion  # noqa: F401
from flask_testing import TestCase

from swagger_server.encoder import JSONEncoder


class BaseTestCase(TestCase):
    def create_app(self):
        logging.getLogger("connexion.operation").setLevel("ERROR")
        app = connexion.App(__name__, specification_dir="../swagger/")
        app.app.json_encoder = JSONEncoder
        app.add_api("swagger.yaml")
        return app.app
