# Copyright 2021 The MLX Contributors
# 
# SPDX-License-Identifier: Apache-2.0 
# coding: utf-8

"""
    MLX API

    MLX API Extension for Kubeflow Pipelines  # noqa: E501

    OpenAPI spec version: 0.1.30-upload-catalog-from-url
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import unittest

import swagger_client
from swagger_client.api.inference_service_api import InferenceServiceApi  # noqa: E501
from swagger_client.rest import ApiException


class TestInferenceServiceApi(unittest.TestCase):
    """InferenceServiceApi unit test stubs"""

    def setUp(self):
        self.api = swagger_client.api.inference_service_api.InferenceServiceApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_service(self):
        """Test case for get_service

        """
        pass

    def test_list_services(self):
        """Test case for list_services

        Gets all KFServing services  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
