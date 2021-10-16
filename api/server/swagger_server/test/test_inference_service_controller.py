# Copyright 2021 The MLX Contributors 
# 
# SPDX-License-Identifier: Apache-2.0 
# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_status import ApiStatus  # noqa: E501
from swagger_server.test import BaseTestCase


class TestInferenceServiceController(BaseTestCase):
    """InferenceServiceController integration test stubs"""

    def test_get_service(self):
        """Test case for get_service

        
        """
        response = self.client.open(
            '/apis/v1alpha1/inferenceservices/{id}'.format(id='id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_services(self):
        """Test case for list_services

        Gets all KFServing services
        """
        query_string = [('namespace', 'namespace_example'),
                        ('label', 'label_example'),
                        ('sort_by', 'name'),
                        ('filter', '{"name": "test"}')]
        response = self.client.open(
            '/apis/v1alpha1/inferenceservices',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
