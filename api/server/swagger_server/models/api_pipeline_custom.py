# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0
# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.api_pipeline_dag import ApiPipelineDAG  # noqa: F401,E501
from swagger_server.models.api_pipeline_inputs import ApiPipelineInputs  # noqa: F401,E501
from swagger_server import util


class ApiPipelineCustom(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, dag: ApiPipelineDAG=None, inputs: ApiPipelineInputs=None, name: str=None, description: str=None):  # noqa: E501
        """ApiPipelineCustom - a model defined in Swagger

        :param dag: The dag of this ApiPipelineCustom.  # noqa: E501
        :type dag: ApiPipelineDAG
        :param inputs: The inputs of this ApiPipelineCustom.  # noqa: E501
        :type inputs: ApiPipelineInputs
        :param name: The name of this ApiPipelineCustom.  # noqa: E501
        :type name: str
        :param description: The description of this ApiPipelineCustom.  # noqa: E501
        :type description: str
        """
        self.swagger_types = {
            'dag': ApiPipelineDAG,
            'inputs': ApiPipelineInputs,
            'name': str,
            'description': str
        }

        self.attribute_map = {
            'dag': 'dag',
            'inputs': 'inputs',
            'name': 'name',
            'description': 'description'
        }

        self._dag = dag
        self._inputs = inputs
        self._name = name
        self._description = description

    @classmethod
    def from_dict(cls, dikt) -> 'ApiPipelineCustom':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The apiPipelineCustom of this ApiPipelineCustom.  # noqa: E501
        :rtype: ApiPipelineCustom
        """
        return util.deserialize_model(dikt, cls)

    @property
    def dag(self) -> ApiPipelineDAG:
        """Gets the dag of this ApiPipelineCustom.


        :return: The dag of this ApiPipelineCustom.
        :rtype: ApiPipelineDAG
        """
        return self._dag

    @dag.setter
    def dag(self, dag: ApiPipelineDAG):
        """Sets the dag of this ApiPipelineCustom.


        :param dag: The dag of this ApiPipelineCustom.
        :type dag: ApiPipelineDAG
        """
        if dag is None:
            raise ValueError("Invalid value for `dag`, must not be `None`")  # noqa: E501

        self._dag = dag

    @property
    def inputs(self) -> ApiPipelineInputs:
        """Gets the inputs of this ApiPipelineCustom.


        :return: The inputs of this ApiPipelineCustom.
        :rtype: ApiPipelineInputs
        """
        return self._inputs

    @inputs.setter
    def inputs(self, inputs: ApiPipelineInputs):
        """Sets the inputs of this ApiPipelineCustom.


        :param inputs: The inputs of this ApiPipelineCustom.
        :type inputs: ApiPipelineInputs
        """

        self._inputs = inputs

    @property
    def name(self) -> str:
        """Gets the name of this ApiPipelineCustom.

        Name of the custom pipeline  # noqa: E501

        :return: The name of this ApiPipelineCustom.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this ApiPipelineCustom.

        Name of the custom pipeline  # noqa: E501

        :param name: The name of this ApiPipelineCustom.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def description(self) -> str:
        """Gets the description of this ApiPipelineCustom.

        Optional description of the custom pipeline  # noqa: E501

        :return: The description of this ApiPipelineCustom.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description: str):
        """Sets the description of this ApiPipelineCustom.

        Optional description of the custom pipeline  # noqa: E501

        :param description: The description of this ApiPipelineCustom.
        :type description: str
        """

        self._description = description
