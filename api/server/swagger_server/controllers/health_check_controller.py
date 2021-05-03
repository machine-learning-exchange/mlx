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
import connexion
import six

from swagger_server.models.api_status import ApiStatus  # noqa: E501
from swagger_server import util


def health_check(check_database=None, check_object_store=None):  # noqa: E501
    """Checks if the server is running

     # noqa: E501

    :param check_database: Test connection to MySQL database
    :type check_database: bool
    :param check_object_store: Test connection to Minio object store
    :type check_object_store: bool

    :rtype: None
    """
    return util.invoke_controller_impl()
