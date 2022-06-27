# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0
# coding: utf-8

from __future__ import absolute_import

from flask import json  # noqa: F401
from six import BytesIO  # noqa: F401

from swagger_server.models.api_component import ApiComponent  # noqa: F401, E501
from swagger_server.models.api_credential import ApiCredential  # noqa: E501
from swagger_server.models.api_status import ApiStatus  # noqa: F401, E501
from swagger_server.test import BaseTestCase


class TestCredentialServiceController(BaseTestCase):
    """CredentialServiceController integration test stubs"""

    def test_create_credentials(self):
        """Test case for create_credentials"""
        body = ApiCredential()
        response = self.client.open(
            "/apis/v1alpha1/credentials",
            method="POST",
            data=json.dumps(body),
            content_type="application/json",
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_delete_credential(self):
        """Test case for delete_credential"""
        response = self.client.open(
            "/apis/v1alpha1/credentials/{id}".format(id="id_example"), method="DELETE"
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_get_credential(self):
        """Test case for get_credential"""
        response = self.client.open(
            "/apis/v1alpha1/credentials/{id}".format(id="id_example"), method="GET"
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))


if __name__ == "__main__":
    import unittest

    unittest.main()
