# Copyright 2021 IBM Corporation
#
# SPDX-License-Identifier: Apache-2.0
# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class ApiModelScript(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, pipeline_stage: str=None, execution_platform: str=None, script_code: str=None):  # noqa: E501
        """ApiModelScript - a model defined in Swagger

        :param pipeline_stage: The pipeline_stage of this ApiModelScript.  # noqa: E501
        :type pipeline_stage: str
        :param execution_platform: The execution_platform of this ApiModelScript.  # noqa: E501
        :type execution_platform: str
        :param script_code: The script_code of this ApiModelScript.  # noqa: E501
        :type script_code: str
        """
        self.swagger_types = {
            'pipeline_stage': str,
            'execution_platform': str,
            'script_code': str
        }

        self.attribute_map = {
            'pipeline_stage': 'pipeline_stage',
            'execution_platform': 'execution_platform',
            'script_code': 'script_code'
        }

        self._pipeline_stage = pipeline_stage
        self._execution_platform = execution_platform
        self._script_code = script_code

    @classmethod
    def from_dict(cls, dikt) -> 'ApiModelScript':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The apiModelScript of this ApiModelScript.  # noqa: E501
        :rtype: ApiModelScript
        """
        return util.deserialize_model(dikt, cls)

    @property
    def pipeline_stage(self) -> str:
        """Gets the pipeline_stage of this ApiModelScript.

        pipeline stage that this code sample applies to, either 'train' or 'serve'  # noqa: E501

        :return: The pipeline_stage of this ApiModelScript.
        :rtype: str
        """
        return self._pipeline_stage

    @pipeline_stage.setter
    def pipeline_stage(self, pipeline_stage: str):
        """Sets the pipeline_stage of this ApiModelScript.

        pipeline stage that this code sample applies to, either 'train' or 'serve'  # noqa: E501

        :param pipeline_stage: The pipeline_stage of this ApiModelScript.
        :type pipeline_stage: str
        """
        if pipeline_stage is None:
            raise ValueError("Invalid value for `pipeline_stage`, must not be `None`")  # noqa: E501

        self._pipeline_stage = pipeline_stage

    @property
    def execution_platform(self) -> str:
        """Gets the execution_platform of this ApiModelScript.

        execution platform that this code sample applies to, i.e. 'kubernetes', 'knative'  # noqa: E501

        :return: The execution_platform of this ApiModelScript.
        :rtype: str
        """
        return self._execution_platform

    @execution_platform.setter
    def execution_platform(self, execution_platform: str):
        """Sets the execution_platform of this ApiModelScript.

        execution platform that this code sample applies to, i.e. 'kubernetes', 'knative'  # noqa: E501

        :param execution_platform: The execution_platform of this ApiModelScript.
        :type execution_platform: str
        """
        if execution_platform is None:
            raise ValueError("Invalid value for `execution_platform`, must not be `None`")  # noqa: E501

        self._execution_platform = execution_platform

    @property
    def script_code(self) -> str:
        """Gets the script_code of this ApiModelScript.

        the source code to run the model in a pipeline stage  # noqa: E501

        :return: The script_code of this ApiModelScript.
        :rtype: str
        """
        return self._script_code

    @script_code.setter
    def script_code(self, script_code: str):
        """Sets the script_code of this ApiModelScript.

        the source code to run the model in a pipeline stage  # noqa: E501

        :param script_code: The script_code of this ApiModelScript.
        :type script_code: str
        """
        if script_code is None:
            raise ValueError("Invalid value for `script_code`, must not be `None`")  # noqa: E501

        self._script_code = script_code
