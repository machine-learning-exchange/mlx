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

from swagger_server.models.api_component import ApiComponent  # noqa: E501
from swagger_server.models.api_credential import ApiCredential  # noqa: E501
from swagger_server.models.api_status import ApiStatus  # noqa: E501
from swagger_server.test import BaseTestCase


class TestCredentialServiceController(BaseTestCase):
    """CredentialServiceController integration test stubs"""

    def test_create_credentials(self):
        """Test case for create_credentials

        
        """
        body = ApiCredential()
        response = self.client.open(
            '/apis/v1alpha1/credentials',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_credential(self):
        """Test case for delete_credential

        
        """
        response = self.client.open(
            '/apis/v1alpha1/credentials/{id}'.format(id='id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_credential(self):
        """Test case for get_credential

        
        """
        response = self.client.open(
            '/apis/v1alpha1/credentials/{id}'.format(id='id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
