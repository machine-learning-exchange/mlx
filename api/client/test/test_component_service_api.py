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
from swagger_client.api.component_service_api import ComponentServiceApi  # noqa: E501
from swagger_client.rest import ApiException


class TestComponentServiceApi(unittest.TestCase):
    """ComponentServiceApi unit test stubs"""

    def setUp(self):
        self.api = swagger_client.api.component_service_api.ComponentServiceApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_approve_components_for_publishing(self):
        """Test case for approve_components_for_publishing

        """
        pass

    def test_create_component(self):
        """Test case for create_component

        """
        pass

    def test_delete_component(self):
        """Test case for delete_component

        """
        pass

    def test_download_component_files(self):
        """Test case for download_component_files

        Returns the component artifacts compressed into a .tgz (.tar.gz) file.  # noqa: E501
        """
        pass

    def test_generate_component_code(self):
        """Test case for generate_component_code

        """
        pass

    def test_get_component(self):
        """Test case for get_component

        """
        pass

    def test_get_component_template(self):
        """Test case for get_component_template

        """
        pass

    def test_list_components(self):
        """Test case for list_components

        """
        pass

    def test_run_component(self):
        """Test case for run_component

        """
        pass

    def test_set_featured_components(self):
        """Test case for set_featured_components

        """
        pass

    def test_upload_component(self):
        """Test case for upload_component

        """
        pass

    def test_upload_component_file(self):
        """Test case for upload_component_file

        """
        pass


if __name__ == '__main__':
    unittest.main()
