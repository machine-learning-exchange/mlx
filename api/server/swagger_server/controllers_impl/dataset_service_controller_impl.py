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
    get_yaml_file_content_from_uploadfile
from swagger_server.data_access.minio_client import store_file, delete_objects, \
    get_file_content_and_url, NoSuchKey, enable_anonymous_read_access, create_tarfile
from swagger_server.data_access.mysql_client import store_data, generate_id, \
    load_data, delete_data, num_rows, update_multiple
from swagger_server.gateways.kubeflow_pipeline_service import generate_dataset_run_script, \
    run_dataset_in_experiment, _host as KFP_HOST
from swagger_server.models.api_dataset import ApiDataset  # noqa: E501
from swagger_server.models.api_generate_code_response import ApiGenerateCodeResponse  # noqa: E501
from swagger_server.models.api_get_template_response import ApiGetTemplateResponse  # noqa: E501
from swagger_server.models.api_list_datasets_response import ApiListDatasetsResponse  # noqa: E501
from swagger_server.models.api_metadata import ApiMetadata
from swagger_server.models.api_parameter import ApiParameter  # noqa: E501
from swagger_server.models.api_run_code_response import ApiRunCodeResponse  # noqa: E501


def approve_datasets_for_publishing(dataset_ids):  # noqa: E501
    """approve_datasets_for_publishing

    :param dataset_ids: Array of dataset IDs to be approved for publishing.
    :type dataset_ids: List[str]

    :rtype: None
    """

    update_multiple(ApiDataset, [], "publish_approved", False)

    if dataset_ids:
        update_multiple(ApiDataset, dataset_ids, "publish_approved", True)

    return None, 200


def create_dataset(body):  # noqa: E501
    """create_dataset

    :param body:
    :type body: dict | bytes

    :rtype: ApiDataset
    """
    if connexion.request.is_json:
        body = ApiDataset.from_dict(connexion.request.get_json())  # noqa: E501

    api_dataset = body

    error = store_data(api_dataset)

    if error:
        return error, 400

    return api_dataset, 200  # TODO: return 201


def delete_dataset(id):  # noqa: E501
    """delete_dataset

    :param id:
    :type id: str

    :rtype: None
    """
    delete_data(ApiDataset, id)

    delete_objects(bucket_name="mlpipeline", prefix=f"datasets/{id}/")

    return f"Dataset {id} was deleted", 200


def download_dataset_files(id, include_generated_code=None):  # noqa: E501
    """
    Returns the dataset artifacts compressed into a .tgz (.tar.gz) file.

    :param id:
    :type id: str
    :param include_generated_code: Include generated run script in download
    :type include_generated_code: bool

    :rtype: file | binary
    """
    tar, bytes_io = create_tarfile(bucket_name="mlpipeline", prefix=f"datasets/{id}/",
                                   file_extensions=[".yaml", ".yml", ".py", ".md"],
                                   keep_open=include_generated_code)

    if len(tar.members) == 0:
        return f"Could not find dataset with id '{id}'", 404

    if include_generated_code:
        generate_code_response, api_status = generate_dataset_code(id)

        if api_status == 200:
            file_content = generate_code_response.script
            file_name = f"run_dataset.py"

            if file_name in tar.getnames():
                file_name = file_name.replace(".py", "_generated.py")

            tarinfo = tarfile.TarInfo(name=file_name)
            tarinfo.size = len(file_content)
            file_obj = BytesIO(file_content.encode('utf-8'))

            tar.addfile(tarinfo, file_obj)

        tar.close()

    return bytes_io.getvalue(), 200, {"Content-Disposition": f"attachment; filename={id}.tgz"}


def generate_dataset_code(id):  # noqa: E501
    """generate_dataset_code

    Generate sample code to use dataset in a pipeline.

    :param id:
    :type id: str

    :rtype: ApiGenerateCodeResponse
    """
    api_datasets: [ApiDataset] = load_data(ApiDataset, filter_dict={"id": id})

    if not api_datasets:
        return f"Dataset with id '{id}' does not exist", 404

    api_dataset = api_datasets[0]

    # TODO: could there be multiple pipeline DSL scripts, how to choose
    # TODO: re-enable check for uploaded script, until then save time by not doing Minio lookup
    # source_code = retrieve_file_content(bucket_name="mlpipeline", prefix=f"datasets/{id}/",
    #                                     file_extensions=[".py"])
    source_code = None

    if not source_code:
        api_template, _ = get_dataset_template(id)
        source_code = generate_dataset_run_script(api_dataset, api_template.url)

    if source_code:
        generate_code_response = ApiGenerateCodeResponse(script=source_code)
        return generate_code_response, 200

    return f"Could not generate source code for dataset {id}", 500


def get_dataset(id):  # noqa: E501
    """get_dataset

    :param id:
    :type id: str

    :rtype: ApiDataset
    """
    api_datasets: [ApiDataset] = load_data(ApiDataset, filter_dict={"id": id})

    if not api_datasets:
        return "Not found", 404

    return api_datasets[0], 200


def get_dataset_template(id):  # noqa: E501
    """get_dataset_template

    :param id:
    :type id: str

    :rtype: ApiGetTemplateResponse
    """
    try:
        template_yaml, url = get_file_content_and_url(bucket_name="mlpipeline",
                                                      prefix=f"datasets/{id}/",
                                                      file_name="template.yaml")
        template_response = ApiGetTemplateResponse(template=template_yaml, url=url)

        return template_response, 200

    except NoSuchKey:

        return f"Dataset template with id '{id}' does not exist", 404

    except Exception as e:

        return str(e), 500


def list_datasets(page_token=None, page_size=None, sort_by=None, filter=None):  # noqa: E501
    """list_datasets

    :param page_token:
    :type page_token: str
    :param page_size:
    :type page_size: int
    :param sort_by: Can be format of \&quot;field_name\&quot;, \&quot;field_name asc\&quot; or \&quot;field_name des\&quot; Ascending by default.
    :type sort_by: str
    :param filter: A string-serialized JSON dictionary containing key-value pairs with name of the object property to apply filter on and the value of the respective property.
    :type filter: str

    :rtype: ApiListDatasetsResponse
    """

    if page_size == 0:
        return {}, 200

    # TODO: do not misuse page_token as MySQL result offset
    offset = int(page_token) if page_token and page_token.isdigit() else 0

    filter_dict = json.loads(filter) if filter else None

    api_datasets: [ApiDataset] = load_data(ApiDataset, filter_dict=filter_dict, sort_by=sort_by,
                                           count=page_size, offset=offset)

    next_page_token = offset + page_size if len(api_datasets) == page_size else None

    total_size = num_rows(ApiDataset)

    if total_size == next_page_token:
        next_page_token = None

    comp_list = ApiListDatasetsResponse(datasets=api_datasets, total_size=total_size,
                                        next_page_token=next_page_token)
    return comp_list, 200


def run_dataset(id, parameters, run_name=None):  # noqa: E501
    """run_dataset

    :param id:
    :type id: str
    :param parameters:
    :type parameters: list[ApiParameter]
    :param run_name: name to identify the run on the Kubeflow Pipelines UI, defaults to component name
    :type run_name: str

    :rtype: ApiRunCodeResponse
    """
    if KFP_HOST == "UNAVAILABLE":
        return f"Kubeflow Pipeline host is 'UNAVAILABLE'", 503

    if connexion.request.is_json:
        parameters = [ApiParameter.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501

    api_dataset, status_code = get_dataset(id)

    if status_code > 200:
        return f"Component with id '{id}' does not exist", 404

    parameter_dict = {p.name: p.value for p in parameters if p.value and p.value.strip() != ""}

    # parameter_errors, status_code = validate_parameters(api_dataset.parameters, parameter_dict)

    # if parameter_errors:
    #     return parameter_errors, status_code

    api_template, _ = get_dataset_template(id)

    enable_anonymous_read_access(bucket_name="mlpipeline", prefix="datasets/*")

    try:
        run_id = run_dataset_in_experiment(api_dataset, api_template.url,
                                           run_name=run_name,
                                           parameters=parameter_dict)
        return ApiRunCodeResponse(run_url=f"/runs/details/{run_id}"), 200

    except Exception as e:
        return f"Error while trying to run dataset {id}: {e}", 500


def set_featured_datasets(dataset_ids):  # noqa: E501
    """set_featured_datasets

    :param dataset_ids: Array of dataset IDs to be featured.
    :type dataset_ids: List[str]

    :rtype: None
    """

    update_multiple(ApiDataset, [], "featured", False)

    if dataset_ids:
        update_multiple(ApiDataset, dataset_ids, "featured", True)

    return None, 200


def upload_dataset(uploadfile: FileStorage, name=None, existing_id=None):  # noqa: E501
    """upload_dataset

    :param uploadfile: The dataset YAML file to upload. Can be a GZip-compressed TAR file (.tgz, .tar.gz) or a YAML file (.yaml, .yml). Maximum size is 32MB.
    :type uploadfile: werkzeug.datastructures.FileStorage
    :param name: 
    :type name: str
    :param existing_id: The ID of a dataset to be replaced, INTERNAL USE ONLY
    :type existing_id: str

    :rtype: ApiDataset
    """
    yaml_file_content = get_yaml_file_content_from_uploadfile(uploadfile)

    return _upload_dataset_yaml(yaml_file_content, name)


def upload_dataset_file(id, uploadfile):  # noqa: E501
    """upload_dataset_file

    :param id: The id of the dataset.
    :type id: str
    :param uploadfile: The file to upload, overwriting existing. Can be a GZip-compressed TAR file (.tgz), a YAML file (.yaml), Python script (.py), or Markdown file (.md)
    :type uploadfile: werkzeug.datastructures.FileStorage

    :rtype: ApiDataset
    """
    # file_type = uploadfile.mimetype
    file_name = uploadfile.filename
    file_ext = file_name.split(".")[-1]

    if file_ext not in ["tgz", "gz", "yaml", "yml", "py", "md"]:
        return f"File extension not supported: '{file_ext}', uploadfile: '{file_name}'.", 501

    if file_ext in ["tgz", "gz", "yaml", "yml"]:
        delete_dataset(id)
        return upload_dataset(uploadfile, existing_id=id)
    else:
        return f"The API method 'upload_dataset_file' is not implemented for file type '{file_ext}'.", 501

    return "Not implemented (yet).", 501


def upload_dataset_from_url(url, name=None, access_token=None):  # noqa: E501
    """upload_dataset_from_url

    :param url: URL pointing to the dataset YAML file.
    :type url: str
    :param name: Optional, the name of the dataset to be created overriding the name in the YAML file.
    :type name: str
    :param access_token: Optional, the Bearer token to access the &#39;url&#39;.
    :type access_token: str

    :rtype: ApiDataset
    """
    yaml_file_content = download_file_content_from_url(url, access_token)

    return _upload_dataset_yaml(yaml_file_content, name)


###############################################################################
#   private helper methods, not swagger-generated
###############################################################################

def _upload_dataset_yaml(yaml_file_content: AnyStr, name=None, existing_id=None):

    yaml_dict = yaml.load(yaml_file_content, Loader=yaml.FullLoader)

    name = name or yaml_dict["name"]
    description = yaml_dict["description"]
    dataset_id = existing_id or generate_id(name=yaml_dict.get("id", name))
    created_at = datetime.now()

    # if yaml_dict.get("id") != dataset_id:
    #     raise ValueError(f"Dataset.id contains non k8s character: {yaml_dict.get('id')}")

    # TODO: re-evaluate if we should use dataset update time as our MLX "created_at" time
    if "updated" in yaml_dict:
        created_at = datetime.strptime(str(yaml_dict["updated"]), "%Y-%m-%d")
    elif "created" in yaml_dict:
        created_at = datetime.strptime(str(yaml_dict["created"]), "%Y-%m-%d")

    license_name = yaml_dict["license"]["name"]
    domain = yaml_dict["domain"]
    format_type = yaml_dict["format"][0]["type"]
    size = yaml_dict["content"][0].get("size")
    version = yaml_dict["version"]
    filter_categories = yaml_dict.get("filter_categories") or dict()

    # # extract number of records and convert thousand separators based on Locale
    # num_records_str = yaml_dict["statistics"]["number_of_records"]
    # num_records_number_str = num_records_str.split()[0]. \
    #     replace("~", ""). \
    #     replace("+", ""). \
    #     replace("k", "000"). \
    #     replace(",", "")  # assumes thousand separators in locale.en_US.UTF-8
    # # locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')  # setting locale does not work reliably in Docker
    # # number_of_records = locale.atoi(num_records_number_str)
    # number_of_records = int(num_records_number_str)
    number_of_records = yaml_dict["content"][0].get("records", 0)

    related_assets = [a["application"].get("asset_id")
                      for a in yaml_dict.get("related_assets", [])
                      if "MLX" in a.get("application", {}).get("name", "")
                      and "asset_id" in a.get("application", {})]

    template_metadata = yaml_dict.get("metadata") or dict()
    metadata = ApiMetadata(annotations=template_metadata.get("annotations"),
                           labels=template_metadata.get("labels"),
                           tags=template_metadata.get("tags") or yaml_dict.get("seo_tags"))

    # TODO: add "version" to ApiDataset

    api_dataset = ApiDataset(
        id=dataset_id,
        created_at=created_at,
        name=name,
        description=description,
        domain=domain,
        format=format_type,
        size=size,
        number_of_records=number_of_records,
        license=license_name,
        metadata=metadata,
        related_assets=related_assets,
        filter_categories=filter_categories
    )

    uuid = store_data(api_dataset)

    api_dataset.id = uuid

    store_file(bucket_name="mlpipeline", prefix=f"datasets/{api_dataset.id}/",
               file_name="template.yaml", file_content=yaml_file_content,
               content_type="text/yaml")

    enable_anonymous_read_access(bucket_name="mlpipeline", prefix="datasets/*")

    return api_dataset, 201
