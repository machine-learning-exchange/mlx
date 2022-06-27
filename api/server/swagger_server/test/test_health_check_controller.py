# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0
# coding: utf-8

from __future__ import absolute_import

from flask import json  # noqa: F401
from six import BytesIO  # noqa: F401

from swagger_server.models.api_status import ApiStatus  # noqa: F401, E501
from swagger_server.test import BaseTestCase


class TestHealthCheckController(BaseTestCase):
    """HealthCheckController integration test stubs"""

    def test_health_check(self):
        """Test case for health_check

        Checks if the server is running
        """
        query_string = [("check_database", True), ("check_object_store", True)]
        response = self.client.open(
            "/apis/v1alpha1/health_check", method="GET", query_string=query_string
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))


if __name__ == "__main__":
    import unittest

    unittest.main()
