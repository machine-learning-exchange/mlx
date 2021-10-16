# Copyright 2021 The MLX Contributors
# 
# SPDX-License-Identifier: Apache-2.0 
# coding: utf-8

from __future__ import absolute_import

from typing import List

from flask import json
from six import BytesIO

from swagger_server.models.api_component import ApiComponent  # noqa: E501
from swagger_server.models.api_generate_code_response import ApiGenerateCodeResponse  # noqa: E501
from swagger_server.models.api_get_template_response import ApiGetTemplateResponse  # noqa: E501
from swagger_server.models.api_list_components_response import ApiListComponentsResponse  # noqa: E501
from swagger_server.models.api_parameter import ApiParameter  # noqa: E501
from swagger_server.models.api_run_code_response import ApiRunCodeResponse  # noqa: E501
from swagger_server.models.api_status import ApiStatus  # noqa: E501
from swagger_server.test import BaseTestCase


class TestComponentServiceController(BaseTestCase):
    """ComponentServiceController integration test stubs"""

    def test_approve_components_for_publishing(self):
        """Test case for approve_components_for_publishing

        
        """
        component_ids = [List[str]()]
        response = self.client.open(
            '/apis/v1alpha1/components/publish_approved',
            method='POST',
            data=json.dumps(component_ids),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_component(self):
        """Test case for create_component

        
        """
        body = ApiComponent()
        response = self.client.open(
            '/apis/v1alpha1/components',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_component(self):
        """Test case for delete_component

        
        """
        response = self.client.open(
            '/apis/v1alpha1/components/{id}'.format(id='id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_download_component_files(self):
        """Test case for download_component_files

        Returns the component artifacts compressed into a .tgz (.tar.gz) file.
        """
        query_string = [('include_generated_code', False)]
        response = self.client.open(
            '/apis/v1alpha1/components/{id}/download'.format(id='id_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_generate_component_code(self):
        """Test case for generate_component_code

        
        """
        response = self.client.open(
            '/apis/v1alpha1/components/{id}/generate_code'.format(id='id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_component(self):
        """Test case for get_component

        
        """
        response = self.client.open(
            '/apis/v1alpha1/components/{id}'.format(id='id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_component_template(self):
        """Test case for get_component_template

        
        """
        response = self.client.open(
            '/apis/v1alpha1/components/{id}/templates'.format(id='id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_components(self):
        """Test case for list_components

        
        """
        query_string = [('page_token', 'page_token_example'),
                        ('page_size', 56),
                        ('sort_by', 'name'),
                        ('filter', '{"name": "test"}')]
        response = self.client.open(
            '/apis/v1alpha1/components',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_run_component(self):
        """Test case for run_component

        
        """
        parameters = [ApiParameter()]
        query_string = [('run_name', 'run_name_example')]
        response = self.client.open(
            '/apis/v1alpha1/components/{id}/run'.format(id='id_example'),
            method='POST',
            data=json.dumps(parameters),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_featured_components(self):
        """Test case for set_featured_components

        
        """
        component_ids = [List[str]()]
        response = self.client.open(
            '/apis/v1alpha1/components/featured',
            method='POST',
            data=json.dumps(component_ids),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_upload_component(self):
        """Test case for upload_component

        
        """
        query_string = [('name', 'name_example')]
        data = dict(uploadfile=(BytesIO(b'some file data'), 'file.txt'))
        response = self.client.open(
            '/apis/v1alpha1/components/upload',
            method='POST',
            data=data,
            content_type='multipart/form-data',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_upload_component_file(self):
        """Test case for upload_component_file

        
        """
        data = dict(uploadfile=(BytesIO(b'some file data'), 'file.txt'))
        response = self.client.open(
            '/apis/v1alpha1/components/{id}/upload'.format(id='id_example'),
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
