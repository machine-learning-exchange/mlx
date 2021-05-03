# Copyright 2021 IBM Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_dataset import ApiDataset  # noqa: E501
from swagger_server.models.api_generate_code_response import ApiGenerateCodeResponse  # noqa: E501
from swagger_server.models.api_get_template_response import ApiGetTemplateResponse  # noqa: E501
from swagger_server.models.api_list_datasets_response import ApiListDatasetsResponse  # noqa: E501
from swagger_server.models.api_status import ApiStatus  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDatasetServiceController(BaseTestCase):
    """DatasetServiceController integration test stubs"""

    def test_approve_datasets_for_publishing(self):
        """Test case for approve_datasets_for_publishing

        
        """
        dataset_ids = [list[str]()]
        response = self.client.open(
            '/apis/v1alpha1/datasets/publish_approved',
            method='POST',
            data=json.dumps(dataset_ids),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_dataset(self):
        """Test case for create_dataset

        
        """
        body = ApiDataset()
        response = self.client.open(
            '/apis/v1alpha1/datasets',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_dataset(self):
        """Test case for delete_dataset

        
        """
        response = self.client.open(
            '/apis/v1alpha1/datasets/{id}'.format(id='id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_download_dataset_files(self):
        """Test case for download_dataset_files

        Returns the dataset artifacts compressed into a .tgz (.tar.gz) file.
        """
        query_string = [('include_generated_code', False)]
        response = self.client.open(
            '/apis/v1alpha1/datasets/{id}/download'.format(id='id_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_generate_dataset_code(self):
        """Test case for generate_dataset_code

        
        """
        response = self.client.open(
            '/apis/v1alpha1/datasets/{id}/generate_code'.format(id='id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_dataset(self):
        """Test case for get_dataset

        
        """
        response = self.client.open(
            '/apis/v1alpha1/datasets/{id}'.format(id='id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_dataset_template(self):
        """Test case for get_dataset_template

        
        """
        response = self.client.open(
            '/apis/v1alpha1/datasets/{id}/templates'.format(id='id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_datasets(self):
        """Test case for list_datasets

        
        """
        query_string = [('page_token', 'page_token_example'),
                        ('page_size', 56),
                        ('sort_by', 'name'),
                        ('filter', '{"name": "test"}')]
        response = self.client.open(
            '/apis/v1alpha1/datasets',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_featured_datasets(self):
        """Test case for set_featured_datasets

        
        """
        dataset_ids = [list[str]()]
        response = self.client.open(
            '/apis/v1alpha1/datasets/featured',
            method='POST',
            data=json.dumps(dataset_ids),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_upload_dataset(self):
        """Test case for upload_dataset

        
        """
        query_string = [('name', 'name_example')]
        data = dict(uploadfile=(BytesIO(b'some file data'), 'file.txt'))
        response = self.client.open(
            '/apis/v1alpha1/datasets/upload',
            method='POST',
            data=data,
            content_type='multipart/form-data',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_upload_dataset_file(self):
        """Test case for upload_dataset_file

        
        """
        data = dict(uploadfile=(BytesIO(b'some file data'), 'file.txt'))
        response = self.client.open(
            '/apis/v1alpha1/datasets/{id}/upload'.format(id='id_example'),
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
