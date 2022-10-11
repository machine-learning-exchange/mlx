# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0
from swagger_server.data_access import minio_client
from swagger_server.data_access import mysql_client
from swagger_server.models.api_status import ApiStatus


def health_check(check_database=None, check_object_store=None):  # noqa: E501
    """
    Checks if the server is running

    :param check_database: Test connection to MySQL database
    :type check_database: bool
    :param check_object_store: Test connection to Minio object store
    :type check_object_store: bool

    :rtype: None
    """
    test_subject = ""

    try:
        if check_database:
            test_subject = "MySQL"
            mysql_client.health_check()

        if check_object_store:
            test_subject = "Minio"
            minio_client.health_check()

        return "Healthy", 200

    except Exception as e:
        error_msg = "{}: {}".format(test_subject, str(e))
        print(error_msg)

        return ApiStatus(error=error_msg), 500
