# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0


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
