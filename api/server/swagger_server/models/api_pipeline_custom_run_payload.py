# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0
# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.api_pipeline_custom import ApiPipelineCustom  # noqa: F401,E501
from swagger_server.models.dictionary import Dictionary  # noqa: F401,E501
from swagger_server import util


class ApiPipelineCustomRunPayload(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, custom_pipeline: ApiPipelineCustom=None, run_parameters: Dictionary=None):  # noqa: E501
        """ApiPipelineCustomRunPayload - a model defined in Swagger

        :param custom_pipeline: The custom_pipeline of this ApiPipelineCustomRunPayload.  # noqa: E501
        :type custom_pipeline: ApiPipelineCustom
        :param run_parameters: The run_parameters of this ApiPipelineCustomRunPayload.  # noqa: E501
        :type run_parameters: Dictionary
        """
        self.swagger_types = {
            'custom_pipeline': ApiPipelineCustom,
            'run_parameters': Dictionary
        }

        self.attribute_map = {
            'custom_pipeline': 'custom_pipeline',
            'run_parameters': 'run_parameters'
        }

        self._custom_pipeline = custom_pipeline
        self._run_parameters = run_parameters

    @classmethod
    def from_dict(cls, dikt) -> 'ApiPipelineCustomRunPayload':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The apiPipelineCustomRunPayload of this ApiPipelineCustomRunPayload.  # noqa: E501
        :rtype: ApiPipelineCustomRunPayload
        """
        return util.deserialize_model(dikt, cls)

    @property
    def custom_pipeline(self) -> ApiPipelineCustom:
        """Gets the custom_pipeline of this ApiPipelineCustomRunPayload.


        :return: The custom_pipeline of this ApiPipelineCustomRunPayload.
        :rtype: ApiPipelineCustom
        """
        return self._custom_pipeline

    @custom_pipeline.setter
    def custom_pipeline(self, custom_pipeline: ApiPipelineCustom):
        """Sets the custom_pipeline of this ApiPipelineCustomRunPayload.


        :param custom_pipeline: The custom_pipeline of this ApiPipelineCustomRunPayload.
        :type custom_pipeline: ApiPipelineCustom
        """

        self._custom_pipeline = custom_pipeline

    @property
    def run_parameters(self) -> Dictionary:
        """Gets the run_parameters of this ApiPipelineCustomRunPayload.


        :return: The run_parameters of this ApiPipelineCustomRunPayload.
        :rtype: Dictionary
        """
        return self._run_parameters

    @run_parameters.setter
    def run_parameters(self, run_parameters: Dictionary):
        """Sets the run_parameters of this ApiPipelineCustomRunPayload.


        :param run_parameters: The run_parameters of this ApiPipelineCustomRunPayload.
        :type run_parameters: Dictionary
        """

        self._run_parameters = run_parameters
