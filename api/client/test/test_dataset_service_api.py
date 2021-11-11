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
from swagger_client.api.dataset_service_api import DatasetServiceApi  # noqa: E501
from swagger_client.rest import ApiException


class TestDatasetServiceApi(unittest.TestCase):
    """DatasetServiceApi unit test stubs"""

    def setUp(self):
        self.api = swagger_client.api.dataset_service_api.DatasetServiceApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_approve_datasets_for_publishing(self):
        """Test case for approve_datasets_for_publishing

        """
        pass

    def test_create_dataset(self):
        """Test case for create_dataset

        """
        pass

    def test_delete_dataset(self):
        """Test case for delete_dataset

        """
        pass

    def test_download_dataset_files(self):
        """Test case for download_dataset_files

        Returns the dataset artifacts compressed into a .tgz (.tar.gz) file.  # noqa: E501
        """
        pass

    def test_generate_dataset_code(self):
        """Test case for generate_dataset_code

        """
        pass

    def test_get_dataset(self):
        """Test case for get_dataset

        """
        pass

    def test_get_dataset_template(self):
        """Test case for get_dataset_template

        """
        pass

    def test_list_datasets(self):
        """Test case for list_datasets

        """
        pass

    def test_set_featured_datasets(self):
        """Test case for set_featured_datasets

        """
        pass

    def test_upload_dataset(self):
        """Test case for upload_dataset

        """
        pass

    def test_upload_dataset_file(self):
        """Test case for upload_dataset_file

        """
        pass


if __name__ == '__main__':
    unittest.main()
