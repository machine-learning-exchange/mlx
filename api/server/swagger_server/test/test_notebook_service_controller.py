# Copyright 2021 The MLX Contributors
# 
# SPDX-License-Identifier: Apache-2.0 
# coding: utf-8

from __future__ import absolute_import

from typing import List

from flask import json
from six import BytesIO

from swagger_server.models.api_generate_code_response import ApiGenerateCodeResponse  # noqa: E501
from swagger_server.models.api_get_template_response import ApiGetTemplateResponse  # noqa: E501
from swagger_server.models.api_list_notebooks_response import ApiListNotebooksResponse  # noqa: E501
from swagger_server.models.api_notebook import ApiNotebook  # noqa: E501
from swagger_server.models.api_run_code_response import ApiRunCodeResponse  # noqa: E501
from swagger_server.models.api_status import ApiStatus  # noqa: E501
from swagger_server.test import BaseTestCase


class TestNotebookServiceController(BaseTestCase):
    """NotebookServiceController integration test stubs"""

    def test_approve_notebooks_for_publishing(self):
        """Test case for approve_notebooks_for_publishing

        
        """
        notebook_ids = [List[str]()]
        response = self.client.open(
            '/apis/v1alpha1/notebooks/publish_approved',
            method='POST',
            data=json.dumps(notebook_ids),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_notebook(self):
        """Test case for create_notebook

        
        """
        body = ApiNotebook()
        response = self.client.open(
            '/apis/v1alpha1/notebooks',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_notebook(self):
        """Test case for delete_notebook

        
        """
        response = self.client.open(
            '/apis/v1alpha1/notebooks/{id}'.format(id='id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_download_notebook_files(self):
        """Test case for download_notebook_files

        Returns the notebook artifacts compressed into a .tgz (.tar.gz) file.
        """
        query_string = [('include_generated_code', False)]
        response = self.client.open(
            '/apis/v1alpha1/notebooks/{id}/download'.format(id='id_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_generate_notebook_code(self):
        """Test case for generate_notebook_code

        
        """
        response = self.client.open(
            '/apis/v1alpha1/notebooks/{id}/generate_code'.format(id='id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_notebook(self):
        """Test case for get_notebook

        
        """
        response = self.client.open(
            '/apis/v1alpha1/notebooks/{id}'.format(id='id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_notebook_template(self):
        """Test case for get_notebook_template

        
        """
        response = self.client.open(
            '/apis/v1alpha1/notebooks/{id}/templates'.format(id='id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_notebooks(self):
        """Test case for list_notebooks

        
        """
        query_string = [('page_token', 'page_token_example'),
                        ('page_size', 56),
                        ('sort_by', 'name'),
                        ('filter', '{"name": "test"}')]
        response = self.client.open(
            '/apis/v1alpha1/notebooks',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_run_notebook(self):
        """Test case for run_notebook

        
        """
        query_string = [('run_name', 'run_name_example')]
        response = self.client.open(
            '/apis/v1alpha1/notebooks/{id}/run'.format(id='id_example'),
            method='POST',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_featured_notebooks(self):
        """Test case for set_featured_notebooks

        
        """
        notebook_ids = [List[str]()]
        response = self.client.open(
            '/apis/v1alpha1/notebooks/featured',
            method='POST',
            data=json.dumps(notebook_ids),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_upload_notebook(self):
        """Test case for upload_notebook

        
        """
        query_string = [('name', 'name_example')]
        data = dict(uploadfile=(BytesIO(b'some file data'), 'file.txt'))
        response = self.client.open(
            '/apis/v1alpha1/notebooks/upload',
            method='POST',
            data=data,
            content_type='multipart/form-data',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_upload_notebook_file(self):
        """Test case for upload_notebook_file

        
        """
        data = dict(uploadfile=(BytesIO(b'some file data'), 'file.txt'))
        response = self.client.open(
            '/apis/v1alpha1/notebooks/{id}/upload'.format(id='id_example'),
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
