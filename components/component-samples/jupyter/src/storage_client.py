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
from minio import Minio
from re import sub


class StorageClient:

    def __init__(self, endpoint_url, access_key, secret_key):
        url = sub(r"https?://", "", endpoint_url)
        self.client = Minio(
            url,
            access_key=access_key,
            secret_key=secret_key,
            secure=False)

    def __create_bucket(self, bucket_name):
        try:
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
        except Exception as err:
            raise Exception("Unable to create new bucket: %s" % bucket_name)

    def upload_file(self, file_name, bucket_name, object_name):
        self.__create_bucket(bucket_name)

        if not object_name:
            object_name = file_name

        try:
            self.client.fput_object(bucket_name, object_name, file_name)
        except Exception as err:
            raise Exception("Unable to upload notebook:\n%s" % err)
