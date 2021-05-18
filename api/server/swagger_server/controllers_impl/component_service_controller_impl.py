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

from swagger_server.controllers_impl import download_file_content_from_url, \
    get_yaml_file_content_from_uploadfile, validate_parameters
from swagger_server.data_access.minio_client import store_file, delete_objects, \
    retrieve_file_content, retrieve_file_content_and_url, enable_anonymous_read_access, \
    create_tarfile
from swagger_server.data_access.mysql_client import store_data, generate_id, load_data, \
    delete_data, num_rows, update_multiple
from swagger_server.gateways.kubeflow_pipeline_service import generate_component_run_script, run_component_in_experiment
from swagger_server.models.api_component import ApiComponent  # noqa: E501
from swagger_server.models.api_generate_code_response import ApiGenerateCodeResponse  # noqa: E501
from swagger_server.models.api_get_template_response import ApiGetTemplateResponse  # noqa: E501
from swagger_server.models.api_list_components_response import ApiListComponentsResponse  # noqa: E501
from swagger_server.models.api_metadata import ApiMetadata
from swagger_server.models.api_parameter import ApiParameter  # noqa: E501
from swagger_server.models.api_run_code_response import ApiRunCodeResponse  # noqa: E501


def approve_components_for_publishing(component_ids):  # noqa: E501
    """approve_components_for_publishing

    :param component_ids: Array of component IDs to be approved for publishing.
    :type component_ids: List[str]

    :rtype: None
    """

    update_multiple(ApiComponent, [], "publish_approved", False)

    if component_ids:
        update_multiple(ApiComponent, component_ids, "publish_approved", True)

    return None, 200


def create_component(body):  # noqa: E501
    """create_component

    :param body:
    :type body: dict | bytes

    :rtype: ApiComponent
    """
    if connexion.request.is_json:
        body = ApiComponent.from_dict(connexion.request.get_json())  # noqa: E501

    api_component = body

    error = store_data(api_component)

    if error:
        return error, 400

    return api_component, 200  # TODO: return 201


def delete_component(id):  # noqa: E501
    """delete_component

    :param id:
    :type id: str

    :rtype: None
    """
    delete_data(ApiComponent, id)

    delete_objects(bucket_name="mlpipeline", prefix=f"components/{id}/")

    return f"Component {id} was deleted", 200


def download_component_files(id, include_generated_code=None):  # noqa: E501
    """
    Returns the component artifacts compressed into a .tgz (.tar.gz) file.

    :param id:
    :type id: str
    :param include_generated_code: Include generated run script in download
    :type include_generated_code: bool

    :rtype: file | binary
    """
    tar, bytes_io = create_tarfile(bucket_name="mlpipeline", prefix=f"components/{id}/",
                                   file_extensions=[".yaml", ".yml", ".py", ".md"],
                                   keep_open=include_generated_code)

    if len(tar.members) == 0:
        return f"Could not find component with id '{id}'", 404

    if include_generated_code:
        generate_code_response, api_status = generate_component_code(id)

        if api_status == 200:
            file_content = generate_code_response.script
            file_name = f"run_component.py"

            if file_name in tar.getnames():
                file_name = file_name.replace(".py", "_generated.py")

            tarinfo = tarfile.TarInfo(name=file_name)
            tarinfo.size = len(file_content)
            file_obj = BytesIO(file_content.encode('utf-8'))

            tar.addfile(tarinfo, file_obj)

        tar.close()

    return bytes_io.getvalue(), 200, {"Content-Disposition": f"attachment; filename={id}.tgz"}


def generate_component_code(id):  # noqa: E501
    """generate_component_code

    :param id:
    :type id: str

    :rtype: ApiGenerateCodeResponse
    """
    api_components: [ApiComponent] = load_data(ApiComponent, filter_dict={"id": id})

    if not api_components:
        return f"Component with id '{id}' does not exist", 404

    api_component = api_components[0]

    source_code = retrieve_file_content(bucket_name="mlpipeline", prefix=f"components/{id}/", file_extensions=[".py"])

    if not source_code:
        api_template, _ = get_component_template(id)
        source_code = generate_component_run_script(api_component, api_template.url)

    if source_code:
        generate_code_response = ApiGenerateCodeResponse(script=source_code)
        return generate_code_response, 200

    else:
        return f"Could not generate source code for component {id}", 500


def get_component(id):  # noqa: E501
    """get_component

    :param id:
    :type id: str

    :rtype: ApiComponent
    """
    api_components: [ApiComponent] = load_data(ApiComponent, filter_dict={"id": id})

    if not api_components:
        return "Not found", 404

    api_component = api_components[0]

    return api_component, 200


def get_component_template(id):  # noqa: E501
    """get_component_template

    :param id:
    :type id: str

    :rtype: ApiGetTemplateResponse
    """
    files_w_url = retrieve_file_content_and_url(bucket_name="mlpipeline", prefix=f"components/{id}/",
                                                file_extensions=[".yaml", ".yml"])
    if files_w_url:
        template_yaml, url = files_w_url[0]
        template_response = ApiGetTemplateResponse(template=template_yaml, url=url)
        return template_response, 200

    else:
        return f"Component template with id '{id}' does not exist", 404


def list_components(page_token=None, page_size=None, sort_by=None, filter=None):  # noqa: E501
    """list_components

    :param page_token:
    :type page_token: str
    :param page_size:
    :type page_size: int
    :param sort_by: Can be format of \&quot;field_name\&quot;, \&quot;field_name asc\&quot; or \&quot;field_name des\&quot; Ascending by default.
    :type sort_by: str
    :param filter: A string-serialized JSON dictionary containing key-value pairs with name of the object property to apply filter on and the value of the respective property.
    :type filter: str

    :rtype: ApiListComponentsResponse
    """

    if page_size == 0:
        return {}, 200

    # TODO: do not misuse page_token as MySQL result offset
    offset = int(page_token) if page_token and page_token.isdigit() else 0

    filter_dict = json.loads(filter) if filter else None

    api_components: [ApiComponent] = load_data(ApiComponent, filter_dict=filter_dict, sort_by=sort_by,
                                               count=page_size, offset=offset)

    next_page_token = offset + page_size if len(api_components) == page_size else None

    total_size = num_rows(ApiComponent)

    if total_size == next_page_token:
        next_page_token = None

    comp_list = ApiListComponentsResponse(components=api_components, total_size=total_size,
                                          next_page_token=next_page_token)
    return comp_list, 200


def run_component(id, parameters, run_name=None):  # noqa: E501
    """run_component

    :param id:
    :type id: str
    :param parameters:
    :type parameters: List[ApiParameter]
    :param run_name: name to identify the run on the Kubeflow Pipelines UI, defaults to component name
    :type run_name: str

    :rtype: ApiRunCodeResponse
    """
    if connexion.request.is_json:
        parameters = [ApiParameter.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501

    parameter_dict = {p.name: p.value for p in parameters if p.value and p.value.strip() != ""}

    api_component, status_code = get_component(id)

    if status_code > 200:
        return f"Component with id '{id}' does not exist", 404

    parameter_errors, status_code = validate_parameters(api_component.parameters, parameter_dict)

    if parameter_errors:
        return parameter_errors, status_code

    api_template, _ = get_component_template(id)

    enable_anonymous_read_access(bucket_name="mlpipeline", prefix="components/*")

    try:
        run_id = run_component_in_experiment(api_component, api_template.url, parameter_dict, run_name)
        return ApiRunCodeResponse(run_url=f"/runs/details/{run_id}"), 200

    except Exception as e:
        return f"Error while trying to run component {id}: {e}", 500


def set_featured_components(component_ids):  # noqa: E501
    """set_featured_components

    :param component_ids: Array of component IDs to be featured.
    :type component_ids: List[str]

    :rtype: None
    """

    update_multiple(ApiComponent, [], "featured", False)

    if component_ids:
        update_multiple(ApiComponent, component_ids, "featured", True)

    return None, 200


def upload_component(uploadfile: FileStorage, name=None, existing_id=None):  # noqa: E501
    """upload_component

    :param uploadfile: The component to upload. Maximum size of 32MB is supported.
    :type uploadfile: werkzeug.datastructures.FileStorage
    :param name: 
    :type name: str
    :param existing_id: The ID of a component to be replaced, INTERNAL USE ONLY
    :type existing_id: str

    :rtype: ApiComponent
    """
    yaml_file_content = get_yaml_file_content_from_uploadfile(uploadfile)

    return _upload_component_yaml(yaml_file_content, name, existing_id)


def upload_component_file(id, uploadfile):  # noqa: E501
    """upload_component_file

    :param id: The id of the component.
    :type id: str
    :param uploadfile: The file to upload, overwriting existing. Can be a GZip-compressed TAR file (.tgz), a YAML file (.yaml), Python script (.py), or Markdown file (.md)
    :type uploadfile: werkzeug.datastructures.FileStorage

    :rtype: ApiComponent
    """
    # file_type = uploadfile.mimetype
    file_name = uploadfile.filename
    file_ext = file_name.split(".")[-1]

    if file_ext not in ["tgz", "gz", "yaml", "yml", "py", "md"]:
        return f"File extension not supported: '{file_ext}', uploadfile: '{file_name}'.", 501

    if file_ext in ["tgz", "gz", "yaml", "yml"]:
        delete_component(id)
        return upload_component(uploadfile, existing_id=id)
    else:
        return f"The API method 'upload_component_file' is not implemented for file type '{file_ext}'.", 501

    return "Not implemented (yet).", 501


def upload_component_from_url(url, name=None, access_token=None):  # noqa: E501
    """upload_component_from_url

    :param url: URL pointing to the component YAML file.
    :type url: str
    :param name: Optional, the name of the component to be created overriding the name in the YAML file.
    :type name: str
    :param access_token: Optional, the Bearer token to access the &#39;url&#39;.
    :type access_token: str

    :rtype: ApiComponent
    """
    yaml_file_content = download_file_content_from_url(url, access_token)

    return _upload_component_yaml(yaml_file_content, name)


###############################################################################
#   private helper methods, not swagger-generated
###############################################################################

def _upload_component_yaml(yaml_file_content: AnyStr, name=None, existing_id=None):

    yaml_dict = yaml.load(yaml_file_content, Loader=yaml.FullLoader)

    template_metadata = yaml_dict.get("metadata") or dict()

    component_id = existing_id or generate_id(name=name or yaml_dict["name"])
    created_at = datetime.now()
    name = name or yaml_dict["name"]
    description = (yaml_dict["description"] or "").strip()[:255]

    metadata = ApiMetadata(annotations=template_metadata.get("annotations"),
                           labels=template_metadata.get("labels"),
                           tags=template_metadata.get("tags"))

    parameters = [ApiParameter(name=p.get("name"), description=p.get("description"),
                               default=p.get("default"), value=p.get("value"))
                  for p in yaml_dict.get("inputs")]

    api_component = ApiComponent(id=component_id,
                                 created_at=created_at,
                                 name=name,
                                 description=description,
                                 metadata=metadata,
                                 parameters=parameters)

    uuid = store_data(api_component)

    api_component.id = uuid

    store_file(bucket_name="mlpipeline", prefix=f"components/{component_id}/",
               file_name="template.yaml", file_content=yaml_file_content)

    enable_anonymous_read_access(bucket_name="mlpipeline", prefix="components/*")

    return api_component, 201
