# Copyright 2021 IBM Corporation 
# 
# SPDX-License-Identifier: Apache-2.0 
# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
# from swagger_server.models.byte_array import ByteArray  # noqa: F401,E501
import re  # noqa: F401,E501
from swagger_server import util


class ProtobufAny(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, type_url: str=None, value:object=None):  # noqa: E501
        """ProtobufAny - a model defined in Swagger

        :param type_url: The type_url of this ProtobufAny.  # noqa: E501
        :type type_url: str
        :param value: The value of this ProtobufAny.  # noqa: E501
        :type value: ByteArray
        """
        self.swagger_types = {
            'type_url': str,
            'value': object
        }

        self.attribute_map = {
            'type_url': 'type_url',
            'value': 'value'
        }

        self._type_url = type_url
        self._value = value

    @classmethod
    def from_dict(cls, dikt) -> 'ProtobufAny':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The protobufAny of this ProtobufAny.  # noqa: E501
        :rtype: ProtobufAny
        """
        return util.deserialize_model(dikt, cls)

    @property
    def type_url(self) -> str:
        """Gets the type_url of this ProtobufAny.

        TODO  # noqa: E501

        :return: The type_url of this ProtobufAny.
        :rtype: str
        """
        return self._type_url

    @type_url.setter
    def type_url(self, type_url: str):
        """Sets the type_url of this ProtobufAny.

        TODO  # noqa: E501

        :param type_url: The type_url of this ProtobufAny.
        :type type_url: str
        """

        self._type_url = type_url

    @property
    def value(self) -> object:
        """Gets the value of this ProtobufAny.

        Must be a valid serialized protocol buffer of the above specified type.  # noqa: E501

        :return: The value of this ProtobufAny.
        :rtype: ByteArray
        """
        return self._value

    @value.setter
    def value(self, value: object):
        """Sets the value of this ProtobufAny.

        Must be a valid serialized protocol buffer of the above specified type.  # noqa: E501

        :param value: The value of this ProtobufAny.
        :type value: ByteArray
        """
        if value is not None and not re.search(r'^(?:[A-Za-z0-9+\/]{4})*(?:[A-Za-z0-9+\/]{2}==|[A-Za-z0-9+\/]{3}=)?$', value):  # noqa: E501
            raise ValueError("Invalid value for `value`, must be a follow pattern or equal to `/^(?:[A-Za-z0-9+\/]{4})*(?:[A-Za-z0-9+\/]{2}==|[A-Za-z0-9+\/]{3}=)?$/`")  # noqa: E501

        self._value = value
