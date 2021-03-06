# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0
# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.any_value import AnyValue  # noqa: F401,E501
from swagger_server import util


class ApiInferenceservice(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, api_version: str=None, kind: str=None, metadata: AnyValue=None, spec: AnyValue=None):  # noqa: E501
        """ApiInferenceservice - a model defined in Swagger

        :param api_version: The api_version of this ApiInferenceservice.  # noqa: E501
        :type api_version: str
        :param kind: The kind of this ApiInferenceservice.  # noqa: E501
        :type kind: str
        :param metadata: The metadata of this ApiInferenceservice.  # noqa: E501
        :type metadata: AnyValue
        :param spec: The spec of this ApiInferenceservice.  # noqa: E501
        :type spec: AnyValue
        """
        self.swagger_types = {
            'api_version': str,
            'kind': str,
            'metadata': AnyValue,
            'spec': AnyValue
        }

        self.attribute_map = {
            'api_version': 'apiVersion',
            'kind': 'kind',
            'metadata': 'metadata',
            'spec': 'spec'
        }

        self._api_version = api_version
        self._kind = kind
        self._metadata = metadata
        self._spec = spec

    @classmethod
    def from_dict(cls, dikt) -> 'ApiInferenceservice':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The apiInferenceservice of this ApiInferenceservice.  # noqa: E501
        :rtype: ApiInferenceservice
        """
        return util.deserialize_model(dikt, cls)

    @property
    def api_version(self) -> str:
        """Gets the api_version of this ApiInferenceservice.


        :return: The api_version of this ApiInferenceservice.
        :rtype: str
        """
        return self._api_version

    @api_version.setter
    def api_version(self, api_version: str):
        """Sets the api_version of this ApiInferenceservice.


        :param api_version: The api_version of this ApiInferenceservice.
        :type api_version: str
        """
        if api_version is None:
            raise ValueError("Invalid value for `api_version`, must not be `None`")  # noqa: E501

        self._api_version = api_version

    @property
    def kind(self) -> str:
        """Gets the kind of this ApiInferenceservice.


        :return: The kind of this ApiInferenceservice.
        :rtype: str
        """
        return self._kind

    @kind.setter
    def kind(self, kind: str):
        """Sets the kind of this ApiInferenceservice.


        :param kind: The kind of this ApiInferenceservice.
        :type kind: str
        """
        if kind is None:
            raise ValueError("Invalid value for `kind`, must not be `None`")  # noqa: E501

        self._kind = kind

    @property
    def metadata(self) -> AnyValue:
        """Gets the metadata of this ApiInferenceservice.


        :return: The metadata of this ApiInferenceservice.
        :rtype: AnyValue
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata: AnyValue):
        """Sets the metadata of this ApiInferenceservice.


        :param metadata: The metadata of this ApiInferenceservice.
        :type metadata: AnyValue
        """

        self._metadata = metadata

    @property
    def spec(self) -> AnyValue:
        """Gets the spec of this ApiInferenceservice.


        :return: The spec of this ApiInferenceservice.
        :rtype: AnyValue
        """
        return self._spec

    @spec.setter
    def spec(self, spec: AnyValue):
        """Sets the spec of this ApiInferenceservice.


        :param spec: The spec of this ApiInferenceservice.
        :type spec: AnyValue
        """

        self._spec = spec
