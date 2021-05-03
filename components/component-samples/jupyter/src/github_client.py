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
from re import sub
import requests


class GithubClient:

    DOMAIN = 'github.com'
    ENTERPRISE_DOMAIN = 'github.ibm.com'
    RAW_DOMAIN = 'raw.githubusercontent.com'
    RAW_ENTERPRISE_DOMAIN = 'raw.github.ibm.com'

    def __init__(self, api_token=None):
        self.headers = GithubClient.__create_headers(api_token)

    @staticmethod
    def __create_headers(api_token):
        if api_token:
            headers = {'Authorization': 'token %s' % api_token}
        else:
            headers = {}
        return headers

    @staticmethod
    def __parse_file_name(url):
        split_url = url.split('/')
        file_name = split_url[-1]
        return file_name

    def __write_response_to_disk(self, response, url):
        if response.status_code != 200:
            raise Exception('Status Code: %d' % response.status_code)

        file_name = self.__parse_file_name(url)
        with open(file_name, 'wb') as fd:
            fd.write(response.content)
        return file_name

    def __is_enterprise(self, url):
        no_protocol_url = sub(r'https?://', '', url)
        domain = no_protocol_url.split('/')[0]
        if domain == self.DOMAIN:
            return False
        return True

    # URLs must be formatted as https://{github.com|github.ibm.com}/path/to/file
    def __parse_github_url(self, url):
        no_blob_url = url.replace(r'/blob', '')
        if self.__is_enterprise(no_blob_url):
            download_url = no_blob_url.replace(self.ENTERPRISE_DOMAIN, self.RAW_ENTERPRISE_DOMAIN)
        else:
            download_url = no_blob_url.replace(self.DOMAIN, self.RAW_DOMAIN)
        return download_url

    def download_file(self, url):
        download_url = self.__parse_github_url(url)
        try:
            response = requests.get(download_url, headers=self.headers)
            file_name = self.__write_response_to_disk(response, download_url)
            return file_name
        except Exception as err:
            raise Exception("Unable to download %s:\n%s" % (url, err))
