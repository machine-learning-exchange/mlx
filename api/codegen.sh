#!/usr/bin/env bash

# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0

SCRIPT_DIR="$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )"

UTIL_FILE="${SCRIPT_DIR}/server/swagger_server/util.py"

cd "$SCRIPT_DIR"

# download the swagger-codegen CLI if it was not installed already
if ! command -v swagger-codegen &> /dev/null; then

    # swagger-codegen requires Java
    if ! command -v java &> /dev/null; then
        echo "Must install Java to run swagger-codegen: https://www.java.com/en/download/help/download_options.html"
        exit 1
    fi

    SWAGGER_VERSION="2.4.8"
    SWAGGER_CODEGEN_CLI_JAR="swagger-codegen-cli-${SWAGGER_VERSION}.jar"

    if [ ! -f "${SWAGGER_CODEGEN_CLI_JAR}" ]; then
        echo "Downloading swagger-codegen ${SWAGGER_VERSION} ..."
        curl -L -O -s "https://repo1.maven.org/maven2/io/swagger/swagger-codegen-cli/${SWAGGER_VERSION}/${SWAGGER_CODEGEN_CLI_JAR}"
    fi

    function swagger-codegen() {
        java -jar "${SWAGGER_CODEGEN_CLI_JAR}" "$@";
    }
    export -f swagger-codegen
fi

swagger-codegen validate -i swagger/swagger.yaml || exit 1

echo "Generating Python client:"
swagger-codegen generate -i swagger/swagger.yaml -l python       -o client 2>&1 | grep -v -E "writing file|/test/" | sed "s|${SCRIPT_DIR}|.|g"

echo "Generating Python server:"
swagger-codegen generate -i swagger/swagger.yaml -l python-flask -o server 2>&1 | grep -v -E "writing file|/test/" | sed "s|${SCRIPT_DIR}|.|g"

# set interactive mode to enable defining a gsed alias
shopt -s expand_aliases

# we use sed to make in-file text replacements, but sed works differently on macOS and Linux
if [[ "$OSTYPE" == "linux-gnu"* ]]; then  # Linux
    alias gsed="sed -i"
elif [[ "$OSTYPE" == "darwin"* ]]; then  # macOS
    alias gsed="sed -i ''"
elif [[ "$OSTYPE" == "cygwin" ]]; then  # POSIX compatible emulation for Windows
    alias gsed="sed -i"
else
    echo "FAILED. OS not compatible with script '${BASH_SOURCE[0]}'"
    exit 1
fi
export gsed

# we need to modify the generated controller methods to 'do some magic!' ...
# replace:
#     return 'do some magic!'
# with:
#     return util.invoke_controller_impl(__name__, locals())
gsed "s/'do some magic\!'/util.invoke_controller_impl()/g" "${SCRIPT_DIR}"/server/swagger_server/controllers/*.py

# and add the 'magic' utility method to forward the controller invocations ... unless we already did
grep "invoke_controller_impl" "${UTIL_FILE}" -q || cat <<'EOF' >> "${UTIL_FILE}"


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


def should_cache(controller_name, method_name):
    return request.method == "GET" \
           and method_name != "health_check" \
           and "inference_service" not in controller_name


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

            if should_cache(controller_name, method_name):
                results = response_cache.get(request_cache_key)

            if not results:
                results = impl_func(**parameters)

                if should_cache(controller_name, method_name):
                    response_cache[request_cache_key] = results
                    log_msg = get_request_log_msg()
                    logging.getLogger("GETcache").info(f"{log_msg} added to cache")

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

EOF

# change back to original working directory
cd -
