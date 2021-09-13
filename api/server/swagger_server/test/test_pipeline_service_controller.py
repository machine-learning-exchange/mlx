# Copyright 2021 IBM Corporation
# 
# SPDX-License-Identifier: Apache-2.0 
# coding: utf-8

from __future__ import absolute_import

from typing import List

from flask import json
from six import BytesIO

from swagger_server.models.api_get_template_response import ApiGetTemplateResponse  # noqa: E501
from swagger_server.models.api_list_pipelines_response import ApiListPipelinesResponse  # noqa: E501
from swagger_server.models.api_pipeline import ApiPipeline  # noqa: E501
from swagger_server.models.api_pipeline_extended import ApiPipelineExtended  # noqa: E501
from swagger_server.models.api_status import ApiStatus  # noqa: E501
from swagger_server.test import BaseTestCase


class TestPipelineServiceController(BaseTestCase):
    """PipelineServiceController integration test stubs"""

    def test_approve_pipelines_for_publishing(self):
        """Test case for approve_pipelines_for_publishing

        
        """
        pipeline_ids = [List[str]()]
        response = self.client.open(
            '/apis/v1alpha1/pipelines/publish_approved',
            method='POST',
            data=json.dumps(pipeline_ids),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_pipeline(self):
        """Test case for create_pipeline

        
        """
        body = ApiPipeline()
        response = self.client.open(
            '/apis/v1alpha1/pipelines',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_pipeline(self):
        """Test case for delete_pipeline

        
        """
        response = self.client.open(
            '/apis/v1alpha1/pipelines/{id}'.format(id='id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_download_pipeline_files(self):
        """Test case for download_pipeline_files

        Returns the pipeline YAML compressed into a .tgz (.tar.gz) file.
        """
        response = self.client.open(
            '/apis/v1alpha1/pipelines/{id}/download'.format(id='id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_pipeline(self):
        """Test case for get_pipeline

        
        """
        response = self.client.open(
            '/apis/v1alpha1/pipelines/{id}'.format(id='id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_template(self):
        """Test case for get_template

        
        """
        response = self.client.open(
            '/apis/v1alpha1/pipelines/{id}/templates'.format(id='id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_pipelines(self):
        """Test case for list_pipelines

        
        """
        query_string = [('page_token', 'page_token_example'),
                        ('page_size', 56),
                        ('sort_by', 'name'),
                        ('filter', '{"name": "test"}')]
        response = self.client.open(
            '/apis/v1alpha1/pipelines',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_featured_pipelines(self):
        """Test case for set_featured_pipelines

        
        """
        pipeline_ids = [List[str]()]
        response = self.client.open(
            '/apis/v1alpha1/pipelines/featured',
            method='POST',
            data=json.dumps(pipeline_ids),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_upload_pipeline(self):
        """Test case for upload_pipeline

        
        """
        query_string = [('name', 'name_example'),
                        ('description', 'description_example')]
        data = dict(uploadfile=(BytesIO(b'some file data'), 'file.txt'),
                    annotations='annotations_example')
        response = self.client.open(
            '/apis/v1alpha1/pipelines/upload',
            method='POST',
            data=data,
            content_type='multipart/form-data',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
