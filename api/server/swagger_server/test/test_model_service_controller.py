# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0
# coding: utf-8

from __future__ import absolute_import

from typing import List

from flask import json
from six import BytesIO

from swagger_server.models.api_generate_model_code_response import (  # noqa: F401
    ApiGenerateModelCodeResponse,
)
from swagger_server.models.api_get_template_response import (  # noqa: F401
    ApiGetTemplateResponse,
)
from swagger_server.models.api_list_models_response import (  # noqa: F401
    ApiListModelsResponse,
)
from swagger_server.models.api_model import ApiModel  # noqa: E501
from swagger_server.models.api_run_code_response import ApiRunCodeResponse  # noqa: F401, E501
from swagger_server.models.api_status import ApiStatus  # noqa: F401, E501
from swagger_server.test import BaseTestCase


class TestModelServiceController(BaseTestCase):
    """ModelServiceController integration test stubs"""

    def test_approve_models_for_publishing(self):
        """Test case for approve_models_for_publishing"""
        model_ids = [List[str]()]
        response = self.client.open(
            "/apis/v1alpha1/models/publish_approved",
            method="POST",
            data=json.dumps(model_ids),
            content_type="application/json",
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_create_model(self):
        """Test case for create_model"""
        body = ApiModel()
        response = self.client.open(
            "/apis/v1alpha1/models",
            method="POST",
            data=json.dumps(body),
            content_type="application/json",
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_delete_model(self):
        """Test case for delete_model"""
        response = self.client.open(
            "/apis/v1alpha1/models/{id}".format(id="id_example"), method="DELETE"
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_download_model_files(self):
        """Test case for download_model_files

        Returns the model artifacts compressed into a .tgz (.tar.gz) file.
        """
        query_string = [("include_generated_code", False)]
        response = self.client.open(
            "/apis/v1alpha1/models/{id}/download".format(id="id_example"),
            method="GET",
            query_string=query_string,
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_generate_model_code(self):
        """Test case for generate_model_code"""
        response = self.client.open(
            "/apis/v1alpha1/models/{id}/generate_code".format(id="id_example"),
            method="GET",
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_get_model(self):
        """Test case for get_model"""
        response = self.client.open(
            "/apis/v1alpha1/models/{id}".format(id="id_example"), method="GET"
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_get_model_template(self):
        """Test case for get_model_template"""
        response = self.client.open(
            "/apis/v1alpha1/models/{id}/templates".format(id="id_example"), method="GET"
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_list_models(self):
        """Test case for list_models"""
        query_string = [
            ("page_token", "page_token_example"),
            ("page_size", 56),
            ("sort_by", "name"),
            ("filter", '{"name": "test"}'),
        ]
        response = self.client.open(
            "/apis/v1alpha1/models", method="GET", query_string=query_string
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_run_model(self):
        """Test case for run_model"""
        query_string = [
            ("pipeline_stage", "pipeline_stage_example"),
            ("execution_platform", "execution_platform_example"),
            ("run_name", "run_name_example"),
        ]
        response = self.client.open(
            "/apis/v1alpha1/models/{id}/run".format(id="id_example"),
            method="POST",
            query_string=query_string,
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_set_featured_models(self):
        """Test case for set_featured_models"""
        model_ids = [List[str]()]
        response = self.client.open(
            "/apis/v1alpha1/models/featured",
            method="POST",
            data=json.dumps(model_ids),
            content_type="application/json",
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_upload_model(self):
        """Test case for upload_model"""
        query_string = [("name", "name_example")]
        data = dict(uploadfile=(BytesIO(b"some file data"), "file.txt"))
        response = self.client.open(
            "/apis/v1alpha1/models/upload",
            method="POST",
            data=data,
            content_type="multipart/form-data",
            query_string=query_string,
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_upload_model_file(self):
        """Test case for upload_model_file"""
        data = dict(uploadfile=(BytesIO(b"some file data"), "file.txt"))
        response = self.client.open(
            "/apis/v1alpha1/models/{id}/upload".format(id="id_example"),
            method="POST",
            data=data,
            content_type="multipart/form-data",
        )
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))


if __name__ == "__main__":
    import unittest

    unittest.main()
