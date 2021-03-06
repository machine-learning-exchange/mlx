# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0
# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class ApiPipelineExtension(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, id: str=None, annotations: Dict[str, str]=None, featured: bool=None, publish_approved: bool=None):  # noqa: E501
        """ApiPipelineExtension - a model defined in Swagger

        :param id: The id of this ApiPipelineExtension.  # noqa: E501
        :type id: str
        :param annotations: The annotations of this ApiPipelineExtension.  # noqa: E501
        :type annotations: Dict[str, str]
        :param featured: The featured of this ApiPipelineExtension.  # noqa: E501
        :type featured: bool
        :param publish_approved: The publish_approved of this ApiPipelineExtension.  # noqa: E501
        :type publish_approved: bool
        """
        self.swagger_types = {
            'id': str,
            'annotations': Dict[str, str],
            'featured': bool,
            'publish_approved': bool
        }

        self.attribute_map = {
            'id': 'id',
            'annotations': 'annotations',
            'featured': 'featured',
            'publish_approved': 'publish_approved'
        }

        self._id = id
        self._annotations = annotations
        self._featured = featured
        self._publish_approved = publish_approved

    @classmethod
    def from_dict(cls, dikt) -> 'ApiPipelineExtension':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The apiPipelineExtension of this ApiPipelineExtension.  # noqa: E501
        :rtype: ApiPipelineExtension
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> str:
        """Gets the id of this ApiPipelineExtension.


        :return: The id of this ApiPipelineExtension.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id: str):
        """Sets the id of this ApiPipelineExtension.


        :param id: The id of this ApiPipelineExtension.
        :type id: str
        """

        self._id = id

    @property
    def annotations(self) -> Dict[str, str]:
        """Gets the annotations of this ApiPipelineExtension.


        :return: The annotations of this ApiPipelineExtension.
        :rtype: Dict[str, str]
        """
        return self._annotations

    @annotations.setter
    def annotations(self, annotations: Dict[str, str]):
        """Sets the annotations of this ApiPipelineExtension.


        :param annotations: The annotations of this ApiPipelineExtension.
        :type annotations: Dict[str, str]
        """

        self._annotations = annotations

    @property
    def featured(self) -> bool:
        """Gets the featured of this ApiPipelineExtension.


        :return: The featured of this ApiPipelineExtension.
        :rtype: bool
        """
        return self._featured

    @featured.setter
    def featured(self, featured: bool):
        """Sets the featured of this ApiPipelineExtension.


        :param featured: The featured of this ApiPipelineExtension.
        :type featured: bool
        """

        self._featured = featured

    @property
    def publish_approved(self) -> bool:
        """Gets the publish_approved of this ApiPipelineExtension.


        :return: The publish_approved of this ApiPipelineExtension.
        :rtype: bool
        """
        return self._publish_approved

    @publish_approved.setter
    def publish_approved(self, publish_approved: bool):
        """Sets the publish_approved of this ApiPipelineExtension.


        :param publish_approved: The publish_approved of this ApiPipelineExtension.
        :type publish_approved: bool
        """

        self._publish_approved = publish_approved
