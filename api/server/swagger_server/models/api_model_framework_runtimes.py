# Copyright 2021 IBM Corporation
#
# SPDX-License-Identifier: Apache-2.0
# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class ApiModelFrameworkRuntimes(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, name: str=None, version: str=None):  # noqa: E501
        """ApiModelFrameworkRuntimes - a model defined in Swagger

        :param name: The name of this ApiModelFrameworkRuntimes.  # noqa: E501
        :type name: str
        :param version: The version of this ApiModelFrameworkRuntimes.  # noqa: E501
        :type version: str
        """
        self.swagger_types = {
            'name': str,
            'version': str
        }

        self.attribute_map = {
            'name': 'name',
            'version': 'version'
        }

        self._name = name
        self._version = version

    @classmethod
    def from_dict(cls, dikt) -> 'ApiModelFrameworkRuntimes':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The apiModelFramework_runtimes of this ApiModelFrameworkRuntimes.  # noqa: E501
        :rtype: ApiModelFrameworkRuntimes
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self) -> str:
        """Gets the name of this ApiModelFrameworkRuntimes.


        :return: The name of this ApiModelFrameworkRuntimes.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this ApiModelFrameworkRuntimes.


        :param name: The name of this ApiModelFrameworkRuntimes.
        :type name: str
        """

        self._name = name

    @property
    def version(self) -> str:
        """Gets the version of this ApiModelFrameworkRuntimes.


        :return: The version of this ApiModelFrameworkRuntimes.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version: str):
        """Sets the version of this ApiModelFrameworkRuntimes.


        :param version: The version of this ApiModelFrameworkRuntimes.
        :type version: str
        """

        self._version = version
