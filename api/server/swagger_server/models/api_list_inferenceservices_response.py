# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0
# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.api_inferenceservice import ApiInferenceservice  # noqa: F401,E501
from swagger_server import util


class ApiListInferenceservicesResponse(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, inferenceservices: List[ApiInferenceservice]=None, total_size: int=None, next_page_token: str=None):  # noqa: E501
        """ApiListInferenceservicesResponse - a model defined in Swagger

        :param inferenceservices: The inferenceservices of this ApiListInferenceservicesResponse.  # noqa: E501
        :type inferenceservices: List[ApiInferenceservice]
        :param total_size: The total_size of this ApiListInferenceservicesResponse.  # noqa: E501
        :type total_size: int
        :param next_page_token: The next_page_token of this ApiListInferenceservicesResponse.  # noqa: E501
        :type next_page_token: str
        """
        self.swagger_types = {
            'inferenceservices': List[ApiInferenceservice],
            'total_size': int,
            'next_page_token': str
        }

        self.attribute_map = {
            'inferenceservices': 'Inferenceservices',
            'total_size': 'total_size',
            'next_page_token': 'next_page_token'
        }

        self._inferenceservices = inferenceservices
        self._total_size = total_size
        self._next_page_token = next_page_token

    @classmethod
    def from_dict(cls, dikt) -> 'ApiListInferenceservicesResponse':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The apiListInferenceservicesResponse of this ApiListInferenceservicesResponse.  # noqa: E501
        :rtype: ApiListInferenceservicesResponse
        """
        return util.deserialize_model(dikt, cls)

    @property
    def inferenceservices(self) -> List[ApiInferenceservice]:
        """Gets the inferenceservices of this ApiListInferenceservicesResponse.


        :return: The inferenceservices of this ApiListInferenceservicesResponse.
        :rtype: List[ApiInferenceservice]
        """
        return self._inferenceservices

    @inferenceservices.setter
    def inferenceservices(self, inferenceservices: List[ApiInferenceservice]):
        """Sets the inferenceservices of this ApiListInferenceservicesResponse.


        :param inferenceservices: The inferenceservices of this ApiListInferenceservicesResponse.
        :type inferenceservices: List[ApiInferenceservice]
        """

        self._inferenceservices = inferenceservices

    @property
    def total_size(self) -> int:
        """Gets the total_size of this ApiListInferenceservicesResponse.


        :return: The total_size of this ApiListInferenceservicesResponse.
        :rtype: int
        """
        return self._total_size

    @total_size.setter
    def total_size(self, total_size: int):
        """Sets the total_size of this ApiListInferenceservicesResponse.


        :param total_size: The total_size of this ApiListInferenceservicesResponse.
        :type total_size: int
        """

        self._total_size = total_size

    @property
    def next_page_token(self) -> str:
        """Gets the next_page_token of this ApiListInferenceservicesResponse.


        :return: The next_page_token of this ApiListInferenceservicesResponse.
        :rtype: str
        """
        return self._next_page_token

    @next_page_token.setter
    def next_page_token(self, next_page_token: str):
        """Sets the next_page_token of this ApiListInferenceservicesResponse.


        :param next_page_token: The next_page_token of this ApiListInferenceservicesResponse.
        :type next_page_token: str
        """

        self._next_page_token = next_page_token
