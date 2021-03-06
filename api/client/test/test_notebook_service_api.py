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
from swagger_client.api.notebook_service_api import NotebookServiceApi  # noqa: E501
from swagger_client.rest import ApiException


class TestNotebookServiceApi(unittest.TestCase):
    """NotebookServiceApi unit test stubs"""

    def setUp(self):
        self.api = swagger_client.api.notebook_service_api.NotebookServiceApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_approve_notebooks_for_publishing(self):
        """Test case for approve_notebooks_for_publishing

        """
        pass

    def test_create_notebook(self):
        """Test case for create_notebook

        """
        pass

    def test_delete_notebook(self):
        """Test case for delete_notebook

        """
        pass

    def test_download_notebook_files(self):
        """Test case for download_notebook_files

        Returns the notebook artifacts compressed into a .tgz (.tar.gz) file.  # noqa: E501
        """
        pass

    def test_generate_notebook_code(self):
        """Test case for generate_notebook_code

        """
        pass

    def test_get_notebook(self):
        """Test case for get_notebook

        """
        pass

    def test_get_notebook_template(self):
        """Test case for get_notebook_template

        """
        pass

    def test_list_notebooks(self):
        """Test case for list_notebooks

        """
        pass

    def test_run_notebook(self):
        """Test case for run_notebook

        """
        pass

    def test_set_featured_notebooks(self):
        """Test case for set_featured_notebooks

        """
        pass

    def test_upload_notebook(self):
        """Test case for upload_notebook

        """
        pass

    def test_upload_notebook_file(self):
        """Test case for upload_notebook_file

        """
        pass


if __name__ == '__main__':
    unittest.main()
