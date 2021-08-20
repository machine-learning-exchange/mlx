# Copyright 2021 IBM Corporation
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import connexion
import json
import tarfile
import yaml

from datetime import datetime
from io import BytesIO
from typing import AnyStr
from werkzeug.datastructures import FileStorage

from swagger_server.controllers_impl import download_file_content_from_url
from swagger_server.controllers_impl import get_yaml_file_content_from_uploadfile
from swagger_server.data_access.minio_client import store_file, delete_objects, \
    get_file_content_and_url, enable_anonymous_read_access, create_tarfile, NoSuchKey
from swagger_server.data_access.mysql_client import store_data, generate_id, \
    load_data, delete_data, num_rows, update_multiple
from swagger_server.gateways.kubeflow_pipeline_service import generate_model_run_script,\
    run_model_in_experiment, _host as KFP_HOST
from swagger_server.models.api_generate_model_code_response import ApiGenerateModelCodeResponse  # noqa: E501
from swagger_server.models.api_get_template_response import ApiGetTemplateResponse  # noqa: E501
from swagger_server.models.api_list_models_response import ApiListModelsResponse  # noqa: E501
from swagger_server.models.api_model import ApiModel  # noqa: E501
from swagger_server.models.api_model_script import ApiModelScript  # noqa: E501
from swagger_server.models.api_run_code_response import ApiRunCodeResponse  # noqa: E501


def approve_models_for_publishing(model_ids):  # noqa: E501
    """approve_models_for_publishing

    :param model_ids: Array of model IDs to be approved for publishing.
    :type model_ids: List[str]

    :rtype: None
    """

    update_multiple(ApiModel, [], "publish_approved", False)

    if model_ids:
        update_multiple(ApiModel, model_ids, "publish_approved", True)

    return None, 200


def create_model(body):  # noqa: E501
    """create_model

    :param body: 
    :type body: dict | bytes

    :rtype: ApiModel
    """
    if connexion.request.is_json:
        body = ApiModel.from_dict(connexion.request.get_json())  # noqa: E501

    api_model = body

    error = store_data(api_model)

    if error:
        return error, 400

    return api_model, 200  # TODO: return 201


def delete_model(id):  # noqa: E501
    """delete_model

    :param id: 
    :type id: str

    :rtype: None
    """
    delete_data(ApiModel, id)

    delete_objects(bucket_name="mlpipeline", prefix=f"models/{id}/")

    return f"Model {id} was deleted", 200


def download_model_files(id, include_generated_code=None):  # noqa: E501
    """
    Returns the model artifacts compressed into a .tgz (.tar.gz) file.

    :param id:
    :type id: str
    :param include_generated_code: Include generated run scripts in download
    :type include_generated_code: bool

    :rtype: file | binary
    """

    tar, bytes_io = create_tarfile(bucket_name="mlpipeline", prefix=f"models/{id}/",
                                   file_extensions=[".yaml", ".yml", ".py", ".md"],
                                   keep_open=include_generated_code)

    if len(tar.members) == 0:
        return f"Could not find model with id '{id}'", 404

    if include_generated_code:
        generate_code_response: ApiGenerateModelCodeResponse = generate_model_code(id)[0]

        for s in generate_code_response.scripts:
            file_name = f"run_{s.pipeline_stage}_{s.execution_platform}.py"

            if file_name in tar.getnames():
                file_name = file_name.replace(".py", "_generated.py")

            file_content = s.script_code
            file_size = len(file_content)
            file_obj = BytesIO(file_content.encode('utf-8'))
            tarinfo = tarfile.TarInfo(name=file_name)
            tarinfo.size = file_size

            tar.addfile(tarinfo, file_obj)

        tar.close()

    return bytes_io.getvalue(), 200, {"Content-Disposition": f"attachment; filename={id}.tgz"}


def generate_model_code(id):  # noqa: E501
    """generate_model_code

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: ApiGenerateModelCodeResponse
    """
    api_models: [ApiModel] = load_data(ApiModel, filter_dict={"id": id})

    if not api_models:
        return f"Model with id '{id}' does not exist", 404

    api_model = api_models[0]

    generate_code_response = ApiGenerateModelCodeResponse(scripts=[])

    source_combinations = []

    if api_model.trainable:
        source_combinations.extend([("train", p) for p in api_model.trainable_tested_platforms])

    if api_model.servable:
        source_combinations.extend([("serve", p) for p in api_model.servable_tested_platforms])

    for stage, platform in source_combinations:
        # TODO: re-enable check for uploaded script, until then save time by not doing Minio lookup
        # source_code = retrieve_file_content(bucket_name="mlpipeline", prefix=f"models/{id}/",
        #                                     file_extensions=[".py"],
        #                                     file_name_filter=f"{stage}_{platform}")
        source_code = None

        if not source_code:
            source_code = generate_model_run_script(api_model, stage, platform)

        api_model_script = ApiModelScript(pipeline_stage=stage,
                                          execution_platform=platform,
                                          script_code=source_code)

        generate_code_response.scripts.append(api_model_script)

    return generate_code_response, 200


def get_model(id):  # noqa: E501
    """get_model

    :param id: 
    :type id: str

    :rtype: ApiModel
    """
    api_models: [ApiModel] = load_data(ApiModel, filter_dict={"id": id})

    if not api_models:
        return "Not found", 404

    return api_models[0], 200


def get_model_template(id):  # noqa: E501
    """get_model_template

    :param id: 
    :type id: str

    :rtype: ApiGetTemplateResponse
    """

    try:
        template_yaml, url = get_file_content_and_url(bucket_name="mlpipeline",
                                                      prefix=f"models/{id}/",
                                                      file_name="template.yaml")
        template_response = ApiGetTemplateResponse(template=template_yaml)

        return template_response, 200

    except NoSuchKey:

        return f"Model template with id '{id}' does not exist", 404

    except Exception as e:

        return str(e), 500


def list_models(page_token=None, page_size=None, sort_by=None, filter=None):  # noqa: E501
    """list_models

    :param page_token: 
    :type page_token: str
    :param page_size: 
    :type page_size: int
    :param sort_by: Can be format of \&quot;field_name\&quot;, \&quot;field_name asc\&quot; or \&quot;field_name des\&quot; Ascending by default.
    :type sort_by: str
    :param filter: A string-serialized JSON dictionary containing key-value pairs with name of the object property to apply filter on and the value of the respective property.
    :type filter: str

    :rtype: ApiListModelsResponse
    """

    if page_size == 0:
        return {}, 200

    # TODO: do not misuse page_token as MySQL result offset
    offset = int(page_token) if page_token and page_token.isdigit() else 0

    filter_dict = json.loads(filter) if filter else None

    api_models: [ApiModel] = load_data(ApiModel,
                                       filter_dict=filter_dict,
                                       sort_by=sort_by,
                                       count=page_size,
                                       offset=offset)

    next_page_token = offset + page_size if len(api_models) == page_size else None

    total_size = num_rows(ApiModel)

    if total_size == next_page_token:
        next_page_token = None

    model_list = ApiListModelsResponse(models=api_models, total_size=total_size, next_page_token=next_page_token)

    return model_list, 200


def run_model(id, pipeline_stage, execution_platform, run_name=None, parameters: dict = None):  # noqa: E501
    """run_model

    :param id: 
    :type id: str
    :param pipeline_stage: pipeline stage, either 'train' or 'serve'
    :type pipeline_stage: str
    :param execution_platform: execution platform, i.e. 'kubernetes', 'knative'
    :type execution_platform: str
    :param run_name: name to identify the run on the Kubeflow Pipelines UI, defaults to model identifier
    :type run_name: str
    :param parameters: optional run parameters, must include 'github_token' and 'github_url' if credentials are required
    :type parameters: dict

    :rtype: ApiRunCodeResponse
    """
    if KFP_HOST == "UNAVAILABLE":
        return f"Kubeflow Pipeline host is 'UNAVAILABLE'", 503

    api_model, status_code = get_model(id)

    if status_code > 200:
        return f"Model with id '{id}' does not exist", 404

    parameter_errors, status_code = _validate_run_parameters(api_model, pipeline_stage, execution_platform, parameters)

    if parameter_errors:
        return parameter_errors, status_code

    try:
        run_id = run_model_in_experiment(api_model, pipeline_stage, execution_platform, run_name, parameters)
        return ApiRunCodeResponse(run_url=f"/runs/details/{run_id}"), 200

    except Exception as e:
        return f"Error while trying to run model with id '{id}': {e}", 500


def set_featured_models(model_ids):  # noqa: E501
    """set_featured_models

    :param model_ids: Array of model IDs to be featured.
    :type model_ids: List[str]

    :rtype: None
    """

    update_multiple(ApiModel, [], "featured", False)

    if model_ids:
        update_multiple(ApiModel, model_ids, "featured", True)

    return None, 200


def upload_model(uploadfile: FileStorage, name=None, existing_id=None):  # noqa: E501
    """upload_model

    :param uploadfile: The model to upload. Maximum size of 32MB is supported.
    :type uploadfile: werkzeug.datastructures.FileStorage
    :param name: 
    :type name: str
    :param existing_id: The model identifier of the model to be replaced, INTERNAL USE ONLY
    :type existing_id: str

    :rtype: ApiModel
    """
    yaml_file_content = get_yaml_file_content_from_uploadfile(uploadfile)

    return _upload_model_yaml(yaml_file_content, name)


def upload_model_file(id, uploadfile):  # noqa: E501
    """upload_model_file

    :param id: The model identifier.
    :type id: str
    :param uploadfile: The file to upload, overwriting existing. Can be a GZip-compressed TAR file (.tgz), a YAML file (.yaml), Python script (.py), or Markdown file (.md)
    :type uploadfile: werkzeug.datastructures.FileStorage

    :rtype: ApiModel
    """
    file_name = uploadfile.filename
    file_ext = file_name.split(".")[-1]

    if file_ext not in ["tgz", "gz", "yaml", "yml", "py", "md"]:
        return f"File extension not supported: '{file_ext}', uploadfile: '{file_name}'.", 501

    if file_ext in ["tgz", "gz", "yaml", "yml"]:
        delete_model(id)
        return upload_model(uploadfile, existing_id=id)
    else:
        return f"The API method 'upload_model_file' is not implemented for file type '{file_ext}'.", 501

    return "Something went wrong?", 500


def upload_model_from_url(url, name=None, access_token=None):  # noqa: E501
    """upload_model_from_url

    :param url: URL pointing to the model YAML file.
    :type url: str
    :param name: Optional, the name of the model to be created overriding the name in the YAML file.
    :type name: str
    :param access_token: Optional, the Bearer token to access the &#39;url&#39;.
    :type access_token: str

    :rtype: ApiModel
    """
    yaml_file_content = download_file_content_from_url(url, access_token)

    return _upload_model_yaml(yaml_file_content, name)


###############################################################################
#   private helper methods, not swagger-generated
###############################################################################

def _upload_model_yaml(yaml_file_content: AnyStr, name=None, existing_id=None):

    model_def = yaml.load(yaml_file_content, Loader=yaml.FullLoader)

    api_model = ApiModel(
        id=existing_id or model_def.get("model_identifier") or generate_id(name=name or model_def["name"]),
        created_at=datetime.now(),
        name=name or model_def["name"],
        description=model_def["description"].strip(),
        domain=model_def.get("domain") or "",
        labels=model_def.get("labels") or dict(),
        framework=model_def["framework"],
        filter_categories=model_def.get("filter_categories") or dict(),
        trainable=model_def.get("train", {}).get("trainable") or False,
        trainable_tested_platforms=model_def.get("train", {}).get("tested_platforms") or [],
        trainable_credentials_required=model_def.get("train", {}).get("credentials_required") or False,
        trainable_parameters=model_def.get("train", {}).get("input_params") or [],
        servable=model_def.get("serve", {}).get("servable") or False,
        servable_tested_platforms=model_def.get("serve", {}).get("tested_platforms") or [],
        servable_credentials_required=model_def.get("serve", {}).get("credentials_required") or False,
        servable_parameters=model_def.get("serve", {}).get("input_params") or [])

    # convert comma-separate strings to lists
    if type(api_model.trainable_tested_platforms) == str:
        api_model.trainable_tested_platforms = api_model.trainable_tested_platforms.replace(", ", ",").split(",")

    if type(api_model.servable_tested_platforms) == str:
        api_model.servable_tested_platforms = api_model.servable_tested_platforms.replace(", ", ",").split(",")

    uuid = store_data(api_model)

    api_model.id = uuid

    store_file(bucket_name="mlpipeline", prefix=f"models/{api_model.id}/",
               file_name="template.yaml", file_content=yaml_file_content,
               content_type="text/yaml")

    enable_anonymous_read_access(bucket_name="mlpipeline", prefix="models/*")

    return api_model, 201


def _validate_run_parameters(api_model: ApiModel, pipeline_stage: str, execution_platform: str, parameters=dict()):

    if pipeline_stage == "train":
        if not api_model.trainable:
            return f"Model '{api_model.id}' is not trainable", 422

        if execution_platform not in api_model.trainable_tested_platforms:
            return f"'{execution_platform}' is not a tested platform to {pipeline_stage} model '{api_model.id}'. " \
                       f"Tested platforms: {api_model.trainable_tested_platforms}", 422

        if api_model.trainable_credentials_required and not {"github_url", "github_token"} <= parameters.keys():
            return f"'github_url' and 'github_token' are required to {pipeline_stage} model '{api_model.id}'", 422

    elif pipeline_stage == "serve":
        if not api_model.servable:
            return f"Model '{api_model.id}' is not servable", 422

        if execution_platform not in api_model.servable_tested_platforms:
            return f"'{execution_platform}' is not a tested platform to {pipeline_stage} model '{api_model.id}'. " \
                       f"Tested platforms: {api_model.servable_tested_platforms}", 422

        if api_model.servable_credentials_required and not {"github_url", "github_token"} <= parameters.keys():
            return f"'github_url' and 'github_token' are required to {pipeline_stage} model '{api_model.id}'", 422

    else:
        return f"Invalid pipeline_stage: '{pipeline_stage}'. Must be one of ['train', 'serve']", 422

    return None, 200
