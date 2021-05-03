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

from swagger_server.models.api_settings import ApiSettings  # noqa: E501
from swagger_server.models.api_status import ApiStatus  # noqa: E501
from swagger_server.models.dictionary import Dictionary  # noqa: E501
from swagger_server.test import BaseTestCase


class TestApplicationSettingsController(BaseTestCase):
    """ApplicationSettingsController integration test stubs"""

    def test_get_application_settings(self):
        """Test case for get_application_settings

        
        """
        response = self.client.open(
            '/apis/v1alpha1/settings',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_modify_application_settings(self):
        """Test case for modify_application_settings

        
        """
        dictionary = Dictionary()
        response = self.client.open(
            '/apis/v1alpha1/settings',
            method='PUT',
            data=json.dumps(dictionary),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_application_settings(self):
        """Test case for set_application_settings

        
        """
        settings = ApiSettings()
        response = self.client.open(
            '/apis/v1alpha1/settings',
            method='POST',
            data=json.dumps(settings),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
