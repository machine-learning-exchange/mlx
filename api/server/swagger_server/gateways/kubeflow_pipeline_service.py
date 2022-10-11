# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0

import autopep8
import json
import os
import re
import yaml

from datetime import datetime

from kfp import Client as KfpClient
from kfp.components._naming import _sanitize_python_function_name as sanitize

from kfp_server_api import ApiRun
from kfp_server_api import ApiPipeline as KfpPipeline
from kfp_server_api.rest import ApiException as PipelineApiException

from os import environ as env
from os.path import abspath, join, dirname
from string import Template

from swagger_server.data_access.mysql_client import generate_id
from swagger_server.data_access.minio_client import get_object_url,\
    create_tarfile, store_file, _host as minio_host, _port as minio_port,\
    _access_key as minio_access_key, _secret_key as minio_secret_key,\
    retrieve_file_content
from swagger_server.models import ApiDataset
from swagger_server.models.api_component import ApiComponent
from swagger_server.models.api_model import ApiModel
from swagger_server.models.api_notebook import ApiNotebook
from swagger_server.models.api_parameter import ApiParameter
from swagger_server.models.api_pipeline import ApiPipeline
from swagger_server.models.api_pipeline_custom import ApiPipelineCustom
from swagger_server.util import ApiError

from time import sleep


CODE_TEMPLATE_DIR = abspath(join(dirname(__file__), "..", "code_templates"))

_namespace = env.get("POD_NAMESPACE", "kubeflow")
_host = env.get("ML_PIPELINE_SERVICE_HOST", "ml-pipeline.%s.svc.cluster.local" % _namespace)
_port = env.get("ML_PIPELINE_SERVICE_PORT", "8888")
_api_base_path = env.get("ML_PIPELINE_SERVICE_API_BASE_PATH", "")
_pipeline_service_url = env.get("ML_PIPELINE_SERVICE_URL", f"{_host}:{_port}/{_api_base_path}".rstrip("/"))


def upload_pipeline_to_kfp(uploadfile: str, name: str = None, description: str = None) -> ApiPipeline:

    kfp_client = KfpClient()

    try:
        kfp_pipeline: KfpPipeline = kfp_client.upload_pipeline(pipeline_package_path=uploadfile,
                                                               pipeline_name=name,
                                                               description=description)
        api_pipeline: ApiPipeline = ApiPipeline.from_dict(kfp_pipeline.to_dict())
        api_pipeline.status = kfp_pipeline.error
        return api_pipeline

    except PipelineApiException as e:
        kfp_host = _pipeline_service_url

        print(f"Error calling PipelineServiceApi ({kfp_host}) -> upload_pipeline(name='{name}'): {e}")

        error_body = json.loads(e.body) or {"error_message": str(e)}
        error_msg = error_body["error_message"]
        status_code = 409 if "already exist. Please specify a new name" in error_msg else e.status

        raise ApiError(error_msg, status_code)

    return None


def delete_kfp_pipeline(pipeline_id: str):

    api_instance = KfpClient()

    try:
        api_instance.delete_pipeline(pipeline_id)

    except AttributeError as e:
        # ignore KFP AttributeError. It is a bug in the Swagger-generated client code for Kubeflow Pipelines
        if not str(e) == "module 'kfp_pipeline.models' has no attribute 'ERRORUNKNOWN'":
            raise e

    except PipelineApiException as e:
        kfp_host = api_instance.api_client.configuration.host
        print(f"Exception when calling PipelineServiceApi ({kfp_host}) -> delete_pipeline: %s\n" % e)
        raise ApiError(message=f"{e.body}\nKFP URL: {kfp_host}", http_status_code=e.status or 422)


def quote_string_value(value):
    if type(value) == str:
        escaped_str = value.replace("'", "\\'")
        return f"'{escaped_str}'"
    else:
        return value


def generate_method_arg_from_parameter(parameter):

    param_name = sanitize(parameter.name)

    if parameter.value or parameter.default:
        value = quote_string_value(parameter.value or parameter.default)
        arg = f"{param_name}={value}"
    elif parameter.value == '' or parameter.default == '':  # TODO: should empty string != None ?
        arg = f"{param_name}=''"
    else:
        arg = param_name

    return arg


def generate_pipeline_method_args(parameters: [ApiParameter]) -> str:
    args = []

    for p in parameters:
        arg = generate_method_arg_from_parameter(p)
        args.append(arg)

    return ",\n        ".join(args)


def generate_component_run_script(component: ApiComponent, component_template_url, run_parameters=dict(),
                                  run_name: str = None):

    name = component.name + " " + generate_id(length=4)
    description = component.description.strip()

    pipeline_method_args = generate_pipeline_method_args(component.parameters)

    parameter_names = ",".join([sanitize(p.name) for p in component.parameters])

    parameter_dict = json.dumps({sanitize(p.name): run_parameters.get(p.name) or p.default or ""
                                 for p in component.parameters},
                                indent=4).replace('"', "'")

    pipeline_server = "" if "POD_NAMESPACE" in os.environ else f"'{_pipeline_service_url}'"

    run_name = (run_name or "").replace("'", "\"") or component.name

    substitutions = dict(locals())

    template_file = f"run_component.TEMPLATE.py"

    with open(join(CODE_TEMPLATE_DIR, template_file), 'r') as f:
        template_raw = f.read()

    template_rendered = Template(template_raw).substitute(substitutions)

    run_script = autopep8.fix_code(template_rendered, options={"aggressive": 2})

    return run_script


def generate_custom_pipeline_function_body(custom_pipeline: ApiPipelineCustom, hide_secrets=True):

    function_body = """
    from kfp import components
    """

    component_template_raw = """
    ${comp_name} = components.load_component_from_url('${template_url}')
    ${op_name} = ${comp_name}(${component_args})
    """

    op_dependency_template_raw = """
    ${op_name}.after(${required_op_name})
    """

    for task in custom_pipeline.dag.tasks:
        parameters = []

        if task.artifact_type == "notebook":
            component_s3_prefix = f"components/jupyter/"
            notebook_url = get_object_url(bucket_name="mlpipeline",
                                          prefix=f"notebooks/{task.artifact_id}/",
                                          file_extensions=[".ipynb"])

            if not notebook_url:
                raise ApiError(f"Could not find notebook '{task.artifact_id}'")

            task_parameters = list(task.arguments.parameters) if task.arguments and task.arguments.parameters else []

            for p in task_parameters:
                if type(p.value) == str and p.value.startswith("{{inputs.parameters."):
                    raise ApiError("Referencing '{{inputs.parameters.*}}' is not supported for notebook parameter"
                                   f" values: {task.to_dict()}", 422)

            notebook_parameters = {p.name: p.value or p.default for p in task_parameters}
            notebook_parameters_str = json.dumps(notebook_parameters) if notebook_parameters else ""

            jupyter_component_parameters = {
                "notebook_url": notebook_url,
                "notebook_params": notebook_parameters_str,
                "api_token": "",
                "endpoint_url": "",
                "bucket_name": "",
                "object_name": "",
                "access_key": "",
                "secret_access_key": ""
            }

            if not hide_secrets:
                output_folder = f"notebooks/{task.artifact_id}/runs/{datetime.now().strftime('%Y%m%d-%H%M%S')}"
                notebook_file_name = notebook_url.split("/")[-1]
                output_file_name = notebook_file_name.replace(r'.ipynb', '_out.ipynb')
                output_file_path = f"{output_folder}/{output_file_name}"
                output_bucket = "mlpipeline"

                jupyter_component_parameters.update({
                    "endpoint_url": "minio-service:9000",  # f"{minio_host}:{minio_port}",
                    "bucket_name": output_bucket,
                    "object_name": output_file_path,
                    "access_key": minio_access_key,
                    "secret_access_key": minio_secret_key
                })

            for name, value in jupyter_component_parameters.items():
                parameters.append(f"{name} = '{value}'")

        elif task.artifact_type == "component":
            component_s3_prefix = f"components/{task.artifact_id}/"

            # replace parameter values that reference pipeline input parameters {{inputs.parameters.parameter_name}}
            task_parameters = list(task.arguments.parameters) if task.arguments and task.arguments.parameters else []

            missing_parameter_values = [p.name for p in task_parameters
                                        if not p.value and not p.default and p.description
                                        and p.description.title().startswith("Required")]

            if missing_parameter_values:
                raise ApiError(f"Missing required task parameters {missing_parameter_values}", 422)

            for p in task_parameters:

                if type(p.value) == str and p.value.startswith("{{inputs.parameters."):
                    match = re.match(r"{{inputs.parameters.(?P<pipeline_parameter_name>\w+)}}", p.value)

                    if not match:
                        raise ApiError(f"Cannot match pipeline input.parameter '{p.value}'", 422)

                    pipeline_param_ref = match.groupdict().get("pipeline_parameter_name")
                    parameters.append(f"{p.name} = {pipeline_param_ref}")

                else:
                    arg = generate_method_arg_from_parameter(p)
                    parameters.append(arg)

        else:
            raise ApiError(f"Unknown or unsupported artifact_type '{task.artifact_type}':\n'{task}'", 422)

        comp_name = "comp_" + re.sub(r"\W+", "_", task.name, flags=re.ASCII).lower()
        op_name = "op_" + re.sub(r"\W+", "_", task.name, flags=re.ASCII).lower()

        template_url = get_object_url(bucket_name="mlpipeline",
                                      prefix=component_s3_prefix,
                                      file_extensions=[".yaml", ".yml"])

        if not template_url:
            raise ApiError(f"Could not find component template '{component_s3_prefix}'")

        substitutions = {
            "comp_name": comp_name,
            "op_name": op_name,
            "template_url": template_url,
            "component_args": ", ".join(parameters)
        }
        template_rendered = Template(component_template_raw).substitute(substitutions)
        function_body += template_rendered

    for task in custom_pipeline.dag.tasks:
        for required_task_name in task.dependencies or []:
            substitutions = {
                "op_name": "op_" + re.sub(r"\W+", "_", task.name, flags=re.ASCII).lower(),
                "required_op_name": "op_" + re.sub(r"\W+", "_", required_task_name, flags=re.ASCII).lower()
            }
            template_rendered = Template(op_dependency_template_raw).substitute(substitutions)
            function_body += template_rendered

    return function_body


def generate_custom_pipeline_run_script(custom_pipeline: ApiPipelineCustom, run_parameters=dict(),
                                        run_name: str = None, hide_secrets=True):

    name = custom_pipeline.name
    description = (custom_pipeline.description or "").strip()

    pipeline_method_args = generate_pipeline_method_args(custom_pipeline.inputs.parameters)

    parameter_dict = json.dumps({p.name: run_parameters.get(p.name) or p.value or p.default  # or ""
                                 for p in custom_pipeline.inputs.parameters},
                                indent=4).replace(': null', ': None')

    pipeline_function_body = generate_custom_pipeline_function_body(custom_pipeline, hide_secrets)

    pipeline_server = "" if "POD_NAMESPACE" in os.environ else f"'{_pipeline_service_url}'"

    run_name = run_name or custom_pipeline.name

    substitutions = dict(locals())

    template_file = f"run_pipeline.TEMPLATE.py"

    with open(join(CODE_TEMPLATE_DIR, template_file), 'r') as f:
        template_raw = f.read()

    template_rendered = Template(template_raw).substitute(substitutions)

    run_script = autopep8.fix_code(template_rendered, options={"aggressive": 2})

    return run_script


def generate_dataset_run_script(dataset: ApiDataset, dataset_template_url, run_parameters=dict(),
                                run_name: str = None, fail_on_missing_prereqs=False):

    name = f"{dataset.name} ({generate_id(length=4)})"
    description = dataset.description.strip().replace("'", "\\'")

    # TODO: some of the parameters, template URLs should move out of here

    # dataset_parameters = dataset.parameters
    # TODO: ApiParameters should not be defined here
    dataset_parameters = [ApiParameter(name="action", default="create"),
                          ApiParameter(name="namespace", default=_namespace)]

    pipeline_method_args = generate_pipeline_method_args(dataset_parameters)

    parameter_names = ",".join([p.name for p in dataset_parameters])

    # TODO: the action parameter is required by DLF-to-PVC op, so it should not be dynamically generated here
    parameter_dict = {
        "action": "create",
        "namespace": run_parameters.get("namespace", _namespace)
    }

    # see component name at
    # https://github.com/machine-learning-exchange/mlx/blob/main/components/component-samples/dax-to-dlf/component.yaml#L1
    dax_to_dlf_component_id = generate_id(name="Generate Dataset Metadata")

    # see component name at https://github.com/machine-learning-exchange/mlx/blob/main/components/component-samples/dlf/component.yaml#L1
    dlf_to_pvc_component_id = generate_id(name="Create Dataset Volume")

    dax_to_dlf_component_url = get_object_url(bucket_name="mlpipeline",
                                              prefix=f"components/{dax_to_dlf_component_id}/",
                                              file_extensions=[".yaml"])

    dlf_to_pvc_component_url = get_object_url(bucket_name="mlpipeline",
                                              prefix=f"components/{dlf_to_pvc_component_id}/",
                                              file_extensions=[".yaml"])

    if fail_on_missing_prereqs:

        if not dax_to_dlf_component_url:
            raise ApiError(f"Missing required component '{dax_to_dlf_component_id}'")

        if not dlf_to_pvc_component_url:
            raise ApiError(f"Missing required component '{dlf_to_pvc_component_id}'")

    namespace = run_parameters.get("namespace", _namespace)

    pipeline_server = "" if "POD_NAMESPACE" in os.environ else f"'{_pipeline_service_url}'"

    run_name = (run_name or "").replace("'", "\"") or dataset.name

    substitutions = dict(locals())

    template_file = f"run_dataset.TEMPLATE.py"

    with open(join(CODE_TEMPLATE_DIR, template_file), 'r') as f:
        template_raw = f.read()

    template_rendered = Template(template_raw).substitute(substitutions)

    run_script = autopep8.fix_code(template_rendered, options={"aggressive": 2})

    return run_script


def generate_model_run_script(model: ApiModel, pipeline_stage: str, execution_platform: str,
                              run_name: str = None, parameters=dict(), hide_secrets=True):

    if pipeline_stage == "serve" and model.servable_credentials_required or \
            pipeline_stage == "train" and model.trainable_credentials_required:

        template_file = f"{pipeline_stage}_{execution_platform.lower()}_w_credentials.TEMPLATE.py"
    else:
        template_file = f"{pipeline_stage}_{execution_platform.lower()}.TEMPLATE.py"

    with open(join(CODE_TEMPLATE_DIR, template_file), 'r') as f:
        template_raw = f.read()

    pipeline_server = "" if "POD_NAMESPACE" in os.environ else f"'{_pipeline_service_url}'"

    substitutions = {
        "model_identifier": model.id,
        "pipeline_server": pipeline_server,
        # "model_name": "maintenance-model-pg", # TODO:  generate_id(name=model.name),
        "run_name": run_name or model.id,
        "generated_secret": "" if hide_secrets else f"secret-{generate_id(length=8).lower()}"
    }

    model_parameters = []

    if pipeline_stage == "train":
        model_parameters = model.trainable_parameters
    elif pipeline_stage == "serve":
        model_parameters = model.servable_parameters

    pipeline_method_args = {p.name: p.value or p.default for p in model_parameters}

    substitutions.update(pipeline_method_args)

    substitutions.update(parameters)

    run_script = Template(template_raw).substitute(substitutions)

    return run_script


def generate_notebook_run_script(api_notebook: ApiNotebook,
                                 parameters: dict = {},
                                 run_name: str = None,
                                 hide_secrets: bool = True):

    if "dataset_pvc" in parameters:
        template_file = "run_notebook_with_dataset.TEMPLATE.py"
    else:
        template_file = "run_notebook.TEMPLATE.py"

    with open(join(CODE_TEMPLATE_DIR, template_file), 'r') as f:
        template_raw = f.read()

    notebook_file = api_notebook.url.split("/")[-1]

    requirements_url = get_object_url(bucket_name="mlpipeline",
                                      prefix=f"notebooks/{api_notebook.id}/",
                                      file_extensions=[".txt"],
                                      file_name_filter="requirements")

    cos_dependencies_archive_url = get_object_url(bucket_name="mlpipeline",
                                                  prefix=f"notebooks/{api_notebook.id}/",
                                                  file_extensions=[".tar.gz"],
                                                  file_name_filter="elyra-dependencies-archive")

    if not cos_dependencies_archive_url:

        tar, bytes_io = create_tarfile(bucket_name="mlpipeline",
                                       prefix=f"notebooks/{api_notebook.id}/",
                                       file_extensions=[".ipynb"])

        cos_dependencies_archive_url = store_file(bucket_name="mlpipeline",
                                                  prefix=f"notebooks/{api_notebook.id}/",
                                                  file_name="elyra-dependencies-archive.tar.gz",
                                                  file_content=bytes_io.getvalue())

    cos_dependencies_archive = cos_dependencies_archive_url.split("/")[-1]

    # TODO: move this into a ApiNotebook.image as opposed to parsing yaml here
    yaml_file_content = retrieve_file_content(bucket_name="mlpipeline",
                                              prefix=f"notebooks/{api_notebook.id}/",
                                              file_extensions=[".yaml", ".yml"])
    metadata_yaml = yaml.load(yaml_file_content, Loader=yaml.FullLoader)

    image = metadata_yaml["implementation"]["github"].get("image", "tensorflow/tensorflow:latest")

    # TODO: elyra-ai/kfp-notebook generates output notebook as: "-output.ipynb"
    #   https://github.com/elyra-ai/kfp-notebook/blob/c8f1298/etc/docker-scripts/bootstrapper.py#L188-L190
    #   so here we may consider renaming the generated file with a datetimestamp
    # output_folder = f"notebooks/{api_notebook.id}/runs/{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    # output_file_name = notebook_file_name.replace(r'.ipynb', '-output.ipynb')
    # output_file_path = f"{output_folder}/{output_file_name}"
    # output_file_url = f"http://{minio_host}:{minio_port}/mlpipeline/{output_file_path}"

    # TODO: do we really need this url:
    #   client = TektonClient(${pipeline_server})
    # vs:
    #   client = TektonClient()
    # ... kfp.Client can figure out the in-cluster IP and port automatically
    kfp_url = f"'{_pipeline_service_url}'" if "POD_NAMESPACE" not in os.environ else ""

    substitutions = {
        "name": api_notebook.name,
        "description": api_notebook.description,
        "notebook": notebook_file,
        "cos_bucket": "mlpipeline",
        "cos_directory": f"notebooks/{api_notebook.id}/",
        "cos_dependencies_archive": cos_dependencies_archive,
        "cos_endpoint": "***",
        "cos_username": "***",
        "cos_password": "***",
        "requirements_url": requirements_url or "",
        "image": image,
        "pipeline_server": kfp_url,
        "run_name": run_name or api_notebook.name
    }

    # TODO: make the `dataset_pvc` and `mount_path` parameters part of the Swagger spec?
    if "dataset_pvc" in parameters:
        substitutions.update({
            "dataset_pvc": parameters["dataset_pvc"],
            "mount_path": parameters.get("mount_path", "/tmp/data")
        })

    if not hide_secrets:
        substitutions.update({
            "cos_endpoint": f"http://{minio_host}:{minio_port}/minio",
            "cos_username": minio_access_key,
            "cos_password": minio_secret_key
        })

    run_script = Template(template_raw).substitute(substitutions)

    return run_script


def run_component_in_experiment(component: ApiComponent, component_template_url: str, parameters: dict,
                                run_name: str = None, wait_for_status: bool = False):

    source_code = generate_component_run_script(component, component_template_url, parameters, run_name)

    return run_code_in_experiment(source_code, wait_for_status)


def run_custom_pipeline_in_experiment(custom_pipeline: ApiPipelineCustom, run_name: str, parameters: dict,
                                      wait_for_status: bool = False):
    try:
        source_code = generate_custom_pipeline_run_script(custom_pipeline, parameters, run_name, hide_secrets=False)

    except Exception as e:
        # TODO: remove this debug logging for development only
        print(f"Error trying to generate code for custom pipeline run '{run_name or custom_pipeline.name}': {e}")
        print(custom_pipeline)
        print(parameters)
        raise e

    try:
        run_id = run_code_in_experiment(source_code, wait_for_status)

    except SyntaxError as e:
        print(f"SyntaxError trying to run pipeline DSL '{run_name or custom_pipeline.name}': {e}")
        print(source_code)
        print("Custom pipeline payload:")
        print(custom_pipeline)
        raise ApiError(f"SyntaxError trying to run pipeline DSL: {e.msg}\n"
                       f"{source_code}",
                       500)

    except Exception as e:
        # TODO: remove this debug logging for development only
        print(f"Error trying to run custom pipeline code '{run_name or custom_pipeline.name}': {e}")
        print(custom_pipeline)
        print(source_code)
        raise e

    # TODO: remove this debug logging for development only
    print("Custom pipeline payload:")
    print(custom_pipeline)
    print("Pipeline DSL:")
    print(source_code)

    return run_id


def run_dataset_in_experiment(dataset: ApiDataset, dataset_template_url: str, parameters: dict = {},
                              run_name: str = None, wait_for_status: bool = False):

    source_code = generate_dataset_run_script(dataset, dataset_template_url, parameters, run_name,
                                              fail_on_missing_prereqs=True)

    return run_code_in_experiment(source_code, wait_for_status)


def run_model_in_experiment(model: ApiModel, pipeline_stage: str, execution_platform: str, run_name: str = None,
                            parameters: dict = None, wait_for_status: bool = False):

    source_code = generate_model_run_script(model, pipeline_stage, execution_platform.lower(), run_name, parameters,
                                            hide_secrets=False)

    return run_code_in_experiment(source_code, wait_for_status)


def run_notebook_in_experiment(notebook: ApiNotebook, parameters: dict, run_name: str,
                               wait_for_status: bool = False):

    source_code = generate_notebook_run_script(notebook, parameters, run_name, hide_secrets=False)

    return run_code_in_experiment(source_code, wait_for_status)


def run_pipeline_in_experiment(api_pipeline: ApiPipeline, parameters: dict = None, run_name: str = None,
                               namespace: str = None, wait_for_status: bool = False):
    try:
        client = KfpClient()
        # if not namespace: ... client._context_setting['namespace'] and client.get_kfp_healthz().multi_user is True:
        experiment = client.create_experiment('PIPELINE_RUNS', namespace=namespace)
        run_result = client.run_pipeline(experiment_id=experiment.id,
                                         job_name=run_name or api_pipeline.name,
                                         params=parameters,
                                         pipeline_id=api_pipeline.id)
        run_id = run_result.id

        if wait_for_status:

            run_details = wait_for_run_status(client, run_id, 10)
            run_status = json.loads(run_details.pipeline_runtime.workflow_manifest)["status"]

            if run_status \
                    and run_status.get("phase", "").lower() in ["failed", "error"] \
                    and run_status.get("message"):
                raise RuntimeError(f"Run {run_id} failed with error: {run_status['message']}")

        return run_id

    except Exception as e:
        print(f"Exception trying to run pipeline {api_pipeline.id} '{api_pipeline.name}'"
              f" with parameters {parameters}:"
              f" %s\n" % e)
        raise ApiError(message=f"{e.body}\nKFP URL: {_pipeline_service_url}", http_status_code=e.status or 422)

    return None


def run_code_in_experiment(source_code: str, wait_for_status=False) -> str:

    exec_locals = dict()

    try:
        exec(source_code, globals(), exec_locals)

    except SyntaxError as e:
        print(f"SyntaxError trying to run_code_in_experiment: {e}")
        print("\n".join(["{}{:3d}: {}".format(">" if n + 1 == e.lineno else " ", n + 1, l)
                         for n, l in enumerate(source_code.splitlines())]))
        # raise ApiError(f"SyntaxError trying to run_code_in_experiment: {e.msg}\n"
        #                f"{source_code}", 500)
        # don't reveal internal code template to users
        raise e

    run_result: ApiRun = exec_locals.get("run_result")

    run_id = run_result.id

    if wait_for_status:

        client: KfpClient = exec_locals['client']
        run_details = wait_for_run_status(client, run_id, 10)
        run_status = json.loads(run_details.pipeline_runtime.workflow_manifest)["status"]

        if run_status \
                and run_status.get("phase", "").lower() in ["failed", "error"] \
                and run_status.get("message"):

            raise RuntimeError(f"Run {run_id} failed with error: {run_status['message']}")

    return run_id


def wait_for_run_status(client, run_id, timeout):

    status = None
    start_time = datetime.now()

    while status is None:

        run_response = client.get_run(run_id=run_id)
        status = run_response.run.status
        elapsed_time = (datetime.now() - start_time).seconds

        if elapsed_time > timeout:
            break

        sleep(1)

    return run_response
