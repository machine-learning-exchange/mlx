# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0
# coding: utf-8

from __future__ import absolute_import

from flask import json  # noqa: F401
from six import BytesIO  # noqa: F401

from swagger_server.models.api_catalog_upload import ApiCatalogUpload  # noqa: F401, E501
from swagger_server.models.api_list_catalog_items_response import (  # noqa: F401
    ApiListCatalogItemsResponse,
)
from swagger_server.models.api_status import ApiStatus  # noqa: F401, E501
from swagger_server.test import BaseTestCase


class TestCatalogServiceController(BaseTestCase):
    """CatalogServiceController integration test stubs"""

    def test_list_all_assets(self):
        """Test case for list_all_assets"""
        query_string = [
            ("page_token", "page_token_example"),
            ("page_size", 56),
            ("sort_by", "sort_by_example"),
            ("filter", "filter_example"),
        ]
        response = self.client.open(
            "/apis/v1alpha1/catalog", method="GET", query_string=query_string
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_upload_multiple_assets(self):
        """Test case for upload_multiple_assets"""
        body = [ApiCatalogUpload()]
        response = self.client.open(
            "/apis/v1alpha1/catalog",
            method="POST",
            data=json.dumps(body),
            content_type="application/json",
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))


if __name__ == "__main__":
    import unittest

    unittest.main()
