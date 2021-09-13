# Copyright 2021 IBM Corporation 
# 
# SPDX-License-Identifier: Apache-2.0 

import datetime
import logging

import six
import typing

from flask import request


def _deserialize(data, klass):
    """Deserializes dict, list, str into an object.

    :param data: dict, list or str.
    :param klass: class literal, or string of class name.

    :return: object.
    """
    if data is None:
        return None

    if klass in six.integer_types or klass in (float, str, bool):
        return _deserialize_primitive(data, klass)
    elif klass == object:
        return _deserialize_object(data)
    elif klass == datetime.date:
        return deserialize_date(data)
    elif klass == datetime.datetime:
        if isinstance(data, datetime.datetime):
            return data
        else:
            return deserialize_datetime(data)
    # AttributeError: module 'typing' has no attribute 'GenericMeta': https://github.com/zalando/connexion/issues/739#issuecomment-437398835
    # elif type(klass) == typing.GenericMeta:
    elif type(klass) == typing._GenericAlias:  # Python >= 3.7
        if klass._name == 'List':
            return _deserialize_list(data, klass.__args__[0])
        if klass._name == 'Dict':
            return _deserialize_dict(data, klass.__args__[1])
    elif hasattr(klass, '__origin__') and hasattr(klass, '__extra__'):  # Python <= 3.6
        if klass.__extra__ == list:
            return _deserialize_list(data, klass.__args__[0])
        if klass.__extra__ == dict:
            return _deserialize_dict(data, klass.__args__[1])
    else:
        return deserialize_model(data, klass)


def _deserialize_primitive(data, klass):
    """Deserializes to primitive type.

    :param data: data to deserialize.
    :param klass: class literal.

    :return: int, long, float, str, bool.
    :rtype: int | long | float | str | bool
    """
    try:
        value = klass(data)
    except UnicodeEncodeError:
        value = six.u(data)
    except TypeError:
        value = data
    return value


def _deserialize_object(value):
    """Return a original value.

    :return: object.
    """
    return value


def deserialize_date(string):
    """Deserializes string to date.

    :param string: str.
    :type string: str
    :return: date.
    :rtype: date
    """
    try:
        from dateutil.parser import parse
        return parse(string).date()
    except ImportError:
        return string


def deserialize_datetime(string):
    """Deserializes string to datetime.

    The string should be in iso8601 datetime format.

    :param string: str.
    :type string: str
    :return: datetime.
    :rtype: datetime
    """
    try:
        from dateutil.parser import parse
        return parse(string)
    except ImportError:
        return string


def deserialize_model(data, klass):
    """Deserializes list or dict to model.

    :param data: dict, list.
    :type data: dict | list
    :param klass: class literal.
    :return: model object.
    """
    instance = klass()

    if not instance.swagger_types:
        return data

    for attr, attr_type in six.iteritems(instance.swagger_types):
        if data is not None \
                and instance.attribute_map[attr] in data \
                and isinstance(data, (list, dict)):
            value = data[instance.attribute_map[attr]]
            setattr(instance, attr, _deserialize(value, attr_type))

    return instance


def _deserialize_list(data, boxed_type):
    """Deserializes a list and its elements.

    :param data: list to deserialize.
    :type data: list
    :param boxed_type: class literal.

    :return: deserialized list.
    :rtype: list
    """
    return [_deserialize(sub_data, boxed_type)
            for sub_data in data]


def _deserialize_dict(data, boxed_type):
    """Deserializes a dict and its elements.

    :param data: dict to deserialize.
    :type data: dict
    :param boxed_type: class literal.

    :return: deserialized dict.
    :rtype: dict
    """
    return {k: _deserialize(v, boxed_type)
            for k, v in six.iteritems(data)}


#######################################################################
#   non-generated methods                                             #
#######################################################################

class ApiError(Exception):

    def __init__(self, message, http_status_code=500):
        self.message = message
        self.http_status_code = http_status_code
        super(ApiError, self).__init__(message)

    def __str__(self):
        return f"{self.message} ({self.http_status_code})"

    def __repr__(self):
        return self.__str__()


# cache results of GET requests, POST/PUT/PATCH/DELETE request will invalidate
response_cache = dict()


def invoke_controller_impl(controller_name=None, parameters=None, method_name=None):
    """
    Invoke the controller implementation of the method called on the parent frame.

    Example in :class:`swagger_server.controllers.component_service_controller` ::

        def delete_component(id):
            return util.invoke_controller_impl(__name__, locals())

    :param controller_name: fully qualified name of the controller, will be
            determined via inspection of the caller frame if not specified

    :param parameters: dictionary of parameters, will be
            determined via inspection of the caller frame if not specified

    :param method_name: name of the method to call on the controller implementation, will be
            determined via inspection of the caller frame if not specified

    :return: result of the controller method execution
    """
    import importlib
    import traceback
    import inspect

    # if not controller_name or not parameters or not method_name:
    if None in (controller_name, parameters, method_name):
        current_frame = inspect.currentframe()
        caller_frame = inspect.getouterframes(current_frame)[1][0]
        caller_module = inspect.getmodule(caller_frame)

        if not controller_name:
            controller_name = caller_module.__name__

        if not method_name:
            method_name = inspect.getframeinfo(caller_frame).function

        if not parameters:
            # caller_func_obj = getattr(caller_module, method_name)
            # parameters = dict(inspect.signature(caller_func_obj).parameters)
            # parameters = inspect.getfullargspec(caller_func_obj).args
            parameters = caller_frame.f_locals

    # replace 'None' values with None, happens when client sets a parameter to None (a JSON serialization quirk)
    for k, v in parameters.items():
        if type(v) == str and v == 'None':
            parameters[k] = None

    # remove parameters with None values, otherwise the default values of method signature will not take effect
    for k, v in dict(parameters).items():
        if v is None:
            del parameters[k]

    module_name_parts = controller_name.split('.')

    if module_name_parts[1] == 'controllers':
        module_name_parts[1] = 'controllers_impl'
        module_name_parts[2] = module_name_parts[2] + '_impl'

    module_name = '.'.join(module_name_parts)

    try:
        controller_impl_module = importlib.import_module(module_name)
        impl_func = getattr(controller_impl_module, method_name)

    except ModuleNotFoundError as e:
        traceback.print_exc()
        return e.msg, 500

    except AttributeError:
        traceback.print_exc()
        return f"The method '{method_name}' does not exist in module '{module_name}'", 501

    if impl_func:
        try:
            results = None
            request_cache_key = (controller_name, method_name, str(parameters))

            if request.method == "GET" and method_name != "health_check":
                results = response_cache.get(request_cache_key)

            if not results:
                results = impl_func(**parameters)

                if request.method == "GET" and method_name != "health_check":
                    response_cache[request_cache_key] = results

                if request.method in ("DELETE", "POST", "PATCH", "PUT") and not method_name.startswith("run_"):
                    # any modifying method clears all cached entries, to avoid loopholes like delete '*',
                    # upload has no 'id', catalog modifies other asset types (represented by controller class), ...
                    response_cache.clear()
                    logging.getLogger("cache").info("Cleared response cache")

            return results

        except ApiError as e:
            print(traceback.format_exc())
            return e.message, e.http_status_code

        except AssertionError as e:
            print(traceback.format_exc())
            return str(e), 422

        # TODO: this is for debugging during development, but we may not want to return details
        #  on just any error in production, revise this!
        except Exception as e:
            print(traceback.format_exc())
            return f"{e.__class__.__name__}: {str(e)}", 500

    else:
        return f'Method not found: {module_name}.{method_name}()', 501

