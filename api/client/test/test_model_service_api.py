# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0
# coding: utf-8

"""
    MLX API

    MLX API Extension for Kubeflow Pipelines  # noqa: E501

    OpenAPI spec version: 0.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import unittest

import swagger_client
from swagger_client.api.model_service_api import ModelServiceApi  # noqa: E501


class TestModelServiceApi(unittest.TestCase):
    """ModelServiceApi unit test stubs"""

    def setUp(self):
        self.api = swagger_client.api.model_service_api.ModelServiceApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_approve_models_for_publishing(self):
        """Test case for approve_models_for_publishing

        """

    def test_create_model(self):
        """Test case for create_model

        """

    def test_delete_model(self):
        """Test case for delete_model

        """

    def test_download_model_files(self):
        """Test case for download_model_files

        Returns the model artifacts compressed into a .tgz (.tar.gz) file.  # noqa: E501
        """

    def test_generate_model_code(self):
        """Test case for generate_model_code

        """

    def test_get_model(self):
        """Test case for get_model

        """

    def test_get_model_template(self):
        """Test case for get_model_template

        """

    def test_list_models(self):
        """Test case for list_models

        """

    def test_run_model(self):
        """Test case for run_model

        """

    def test_set_featured_models(self):
        """Test case for set_featured_models

        """

    def test_upload_model(self):
        """Test case for upload_model

        """

    def test_upload_model_file(self):
        """Test case for upload_model_file

        """


if __name__ == '__main__':
    unittest.main()
