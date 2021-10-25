# Copyright 2021 The MLX Contributors
# 
# SPDX-License-Identifier: Apache-2.0

import connexion
import json
import requests
import tarfile
import yaml

from datetime import datetime
from io import BytesIO
from os import environ as env
from typing import AnyStr
from urllib.parse import urlparse
from werkzeug.datastructures import FileStorage

from swagger_server.controllers_impl import download_file_content_from_url, \
    get_yaml_file_content_from_uploadfile, validate_parameters
from swagger_server.data_access.minio_client import store_file, delete_objects, \
    get_file_content_and_url, enable_anonymous_read_access, NoSuchKey, \
    create_tarfile, get_object_url
from swagger_server.data_access.mysql_client import store_data, generate_id, \
    load_data, delete_data, num_rows, update_multiple
from swagger_server.gateways.kubeflow_pipeline_service import generate_notebook_run_script,\
    run_notebook_in_experiment, _host as KFP_HOST
from swagger_server.models.api_generate_code_response import ApiGenerateCodeResponse  # noqa: E501
from swagger_server.models.api_get_template_response import ApiGetTemplateResponse  # noqa: E501
from swagger_server.models.api_list_notebooks_response import ApiListNotebooksResponse  # noqa: E501
from swagger_server.models.api_metadata import ApiMetadata
from swagger_server.models.api_notebook import ApiNotebook  # noqa: E501
from swagger_server.models.api_parameter import ApiParameter  # noqa: E501
from swagger_server.models.api_run_code_response import ApiRunCodeResponse  # noqa: E501
from swagger_server.util import ApiError


ghe_api_token = env.get("IBM_GHE_API_TOKEN")


def approve_notebooks_for_publishing(notebook_ids):  # noqa: E501
    """approve_notebooks_for_publishing

    :param notebook_ids: Array of notebook IDs to be approved for publishing.
    :type notebook_ids: List[str]

    :rtype: None
    """

    update_multiple(ApiNotebook, [], "publish_approved", False)

    if notebook_ids:
        update_multiple(ApiNotebook, notebook_ids, "publish_approved", True)

    return None, 200


def create_notebook(body):  # noqa: E501
    """create_notebook

    :param body: 
    :type body: dict | bytes

    :rtype: ApiNotebook
    """
    if connexion.request.is_json:
        body = ApiNotebook.from_dict(connexion.request.get_json())  # noqa: E501

    api_notebook = body

    error = store_data(api_notebook)

    if error:
        return error, 400

    return api_notebook, 200  # TODO: return 201


def delete_notebook(id):  # noqa: E501
    """delete_notebook

    :param id: 
    :type id: str

    :rtype: None
    """
    delete_data(ApiNotebook, id)

    delete_objects(bucket_name="mlpipeline", prefix=f"notebooks/{id}/")

    return f"Notebook {id} was deleted", 200


def download_notebook_files(id, include_generated_code=None):  # noqa: E501
    """Returns the notebook artifacts compressed into a .tgz (.tar.gz) file.

    :param id: 
    :type id: str
    :param include_generated_code: Include generated run script in download
    :type include_generated_code: bool

    :rtype: file | binary
    """
    tar, bytes_io = create_tarfile(bucket_name="mlpipeline", prefix=f"notebooks/{id}/",
                                   file_extensions=[".yaml", ".yml", ".py", ".md"],
                                   keep_open=include_generated_code)

    if len(tar.members) == 0:
        return f"Could not find notebook with id '{id}'", 404

    if include_generated_code:
        generate_code_response, api_status = generate_notebook_code(id)

        if api_status == 200:
            file_content = generate_code_response.script
            file_name = f"run_notebook.py"

            if file_name in tar.getnames():
                file_name = file_name.replace(".py", "_generated.py")

            tarinfo = tarfile.TarInfo(name=file_name)
            tarinfo.size = len(file_content)
            file_obj = BytesIO(file_content.encode('utf-8'))

            tar.addfile(tarinfo, file_obj)

        tar.close()

    return bytes_io.getvalue(), 200, {"Content-Disposition": f"attachment; filename={id}.tgz"}


def generate_notebook_code(id):  # noqa: E501
    """generate_notebook_code

    :param id: 
    :type id: str

    :rtype: ApiGenerateCodeResponse
    """
    api_notebooks: [ApiNotebook] = load_data(ApiNotebook, filter_dict={"id": id})

    if not api_notebooks:
        return f"Notebook with id '{id}' does not exist", 404

    api_notebook = api_notebooks[0]

    # TODO: re-enable check for uploaded script, until then save time by not doing Minio lookup
    # source_code = retrieve_file_content(bucket_name="mlpipeline", prefix=f"notebooks/{id}/",
    #                                     file_extensions=[".py"])
    source_code = None

    if not source_code:
        source_code = generate_notebook_run_script(api_notebook)

    if source_code:
        generate_code_response = ApiGenerateCodeResponse(script=source_code)
        return generate_code_response, 200

    else:
        return f"Could not generate source code for notebook {id}", 500


def get_notebook(id):
    """get_notebook

    :param id: 
    :type id: str

    :rtype: ApiNotebook
    """
    api_notebooks: [ApiNotebook] = load_data(ApiNotebook, filter_dict={"id": id})

    if not api_notebooks:
        return "Not found", 404

    return api_notebooks[0], 200


def get_notebook_template(id):  # noqa: E501
    """get_notebook_template

    :param id: 
    :type id: str

    :rtype: ApiGetTemplateResponse
    """
    try:
        template_yaml, url = get_file_content_and_url(bucket_name="mlpipeline", prefix=f"notebooks/{id}/",
                                                      file_name="template.yaml")
        template_response = ApiGetTemplateResponse(template=template_yaml, url=url)

        return template_response, 200

    except NoSuchKey:

        return f"Notebook template with id '{id}' does not exist", 404

    except Exception as e:

        return str(e), 500


def list_notebooks(page_token=None, page_size=None, sort_by=None, filter=None):  # noqa: E501
    """list_notebooks

    :param page_token: 
    :type page_token: str
    :param page_size: 
    :type page_size: int
    :param sort_by: Can be format of \&quot;field_name\&quot;, \&quot;field_name asc\&quot; or \&quot;field_name des\&quot; Ascending by default.
    :type sort_by: str
    :param filter: A string-serialized JSON dictionary containing key-value pairs with name of the object property to apply filter on and the value of the respective property.
    :type filter: str

    :rtype: ApiListNotebooksResponse
    """

    if page_size == 0:
        return {}, 200

    # TODO: do not misuse page_token as MySQL result offset
    offset = int(page_token) if page_token and page_token.isdigit() else 0

    filter_dict = json.loads(filter) if filter else None

    api_notebooks: [ApiNotebook] = load_data(ApiNotebook, filter_dict=filter_dict, sort_by=sort_by,
                                             count=page_size, offset=offset)

    next_page_token = offset + page_size if len(api_notebooks) == page_size else None

    total_size = num_rows(ApiNotebook)

    if total_size == next_page_token:
        next_page_token = None

    notebooks = ApiListNotebooksResponse(notebooks=api_notebooks, total_size=total_size,
                                         next_page_token=next_page_token)
    return notebooks, 200


def run_notebook(id, run_name=None, parameters: dict = None):  # noqa: E501
    """run_notebook

    :param id: 
    :type id: str
    :param run_name: name to identify the run on the Kubeflow Pipelines UI, defaults to notebook name
    :type run_name: str
    :param parameters: optional run parameters, may be required based on pipeline definition
    :type parameters: dict

    :rtype: ApiRunCodeResponse
    """
    if KFP_HOST == "UNAVAILABLE":
        return f"Kubeflow Pipeline host is 'UNAVAILABLE'", 503

    if not parameters and connexion.request.is_json:
        parameter_dict = dict(connexion.request.get_json())  # noqa: E501
    else:
        parameter_dict = parameters

    api_notebook, status_code = get_notebook(id)

    if status_code > 200:
        return f"Notebook with id '{id}' does not exist", 404

    # # TODO: Elyra kfp-notebook currently does not pass parameters on to papermill
    # if parameters:
    #     raise ApiError("The 'elyra-ai/kfp-notebook' executor does not support parameters", 422)

    # parameter_errors, status_code = validate_parameters(api_notebook.parameters, parameter_dict)
    #
    # if parameter_errors:
    #     return parameter_errors, status_code

    # Elyra pulls the requirements.txt from Minio, requiring anonymous read access
    enable_anonymous_read_access(bucket_name="mlpipeline", prefix="notebooks/*")

    try:
        run_id = run_notebook_in_experiment(notebook=api_notebook,
                                            parameters=parameter_dict,
                                            run_name=run_name)

        # expected output notebook based on:
        #   https://github.com/elyra-ai/kfp-notebook/blob/c8f1298/etc/docker-scripts/bootstrapper.py#L188-L190
        notebook_url = get_object_url(bucket_name="mlpipeline",
                                      prefix=f"notebooks/{api_notebook.id}/",
                                      file_extensions=[".ipynb"])
        # TODO: create a "sandboxed" notebook in a subfolder since Elyra overwrites
        #   the original notebook instead of creating an "-output.ipynb" file:
        #   https://github.com/elyra-ai/kfp-notebook/blob/c8f1298/etc/docker-scripts/bootstrapper.py#L205
        notebook_output_url = notebook_url.replace(".ipynb", "-output.ipynb")

        # instead return link to the generated output .html for the time being
        notebook_output_html = notebook_url.replace(".ipynb", ".html")

        return ApiRunCodeResponse(run_url=f"/runs/details/{run_id}",
                                  run_output_location=notebook_output_html), 200
    except Exception as e:

        return f"Error while trying to run notebook {id}: {e}", 500


def set_featured_notebooks(notebook_ids):  # noqa: E501
    """set_featured_notebooks

    :param notebook_ids: Array of notebook IDs to be featured.
    :type notebook_ids: List[str]

    :rtype: None
    """

    update_multiple(ApiNotebook, [], "featured", False)

    if notebook_ids:
        update_multiple(ApiNotebook, notebook_ids, "featured", True)

    return None, 200


def upload_notebook(uploadfile: FileStorage, name=None, enterprise_github_token=None, existing_id=None):  # noqa: E501
    """upload_notebook

    :param uploadfile: The notebook to upload. Maximum size of 32MB is supported.
    :type uploadfile: werkzeug.datastructures.FileStorage
    :param name: 
    :type name: str
    :param enterprise_github_token: Optional GitHub API token providing read-access to notebooks stored on Enterprise GitHub accounts.
    :type enterprise_github_token: str
    :param existing_id: The ID of a notebook to be replaced, INTERNAL USE ONLY
    :type existing_id: str

    :rtype: ApiNotebook
    """
    yaml_file_content = get_yaml_file_content_from_uploadfile(uploadfile)

    return _upload_notebook_yaml(yaml_file_content, name, enterprise_github_token)


def upload_notebook_file(id, uploadfile):  # noqa: E501
    """upload_notebook_file

    :param id: The id of the notebook.
    :type id: str
    :param uploadfile: The file to upload, overwriting existing. Can be a GZip-compressed TAR file (.tgz), a YAML file (.yaml), Python script (.py), or Markdown file (.md)
    :type uploadfile: werkzeug.datastructures.FileStorage

    :rtype: ApiNotebook
    """
    # file_type = uploadfile.mimetype
    file_name = uploadfile.filename
    file_ext = file_name.split(".")[-1]

    if file_ext not in ["tgz", "gz", "yaml", "yml", "py", "md"]:
        return f"File extension not supported: '{file_ext}', uploadfile: '{file_name}'.", 501

    if file_ext in ["tgz", "gz", "yaml", "yml"]:
        delete_notebook(id)
        return upload_notebook(uploadfile, existing_id=id)
    else:
        return f"The API method 'upload_notebook_file' is not implemented for file type '{file_ext}'.", 501

    return "Not implemented (yet).", 501


def upload_notebook_from_url(url, name=None, access_token=None):  # noqa: E501
    """upload_notebook_from_url

    :param url: URL pointing to the notebook YAML file.
    :type url: str
    :param name: Optional, the name of the notebook to be created overriding the name in the YAML file.
    :type name: str
    :param access_token: Optional, the Bearer token to access the &#39;url&#39;.
    :type access_token: str

    :rtype: ApiNotebook
    """
    yaml_file_content = download_file_content_from_url(url, access_token)

    return _upload_notebook_yaml(yaml_file_content, name, access_token)


###############################################################################
#   private helper methods, not swagger-generated
###############################################################################

def _upload_notebook_yaml(yaml_file_content: AnyStr, name=None, access_token=None, existing_id=None):

    yaml_dict = yaml.load(yaml_file_content, Loader=yaml.FullLoader)

    template_metadata = yaml_dict.get("metadata") or dict()

    notebook_id = existing_id or generate_id(name=name or yaml_dict["name"])
    created_at = datetime.now()
    name = name or yaml_dict["name"]
    description = yaml_dict["description"].strip()
    url = yaml_dict["implementation"]["github"]["source"]
    requirements = yaml_dict["implementation"]["github"].get("requirements")
    filter_categories = yaml_dict.get("filter_categories") or dict()

    metadata = ApiMetadata(annotations=template_metadata.get("annotations"),
                           labels=template_metadata.get("labels"),
                           tags=template_metadata.get("tags"))

    notebook_content = _download_notebook(url, enterprise_github_api_token=access_token)

    # parameters = _extract_notebook_parameters(notebook_content)
    # TODO: not using Papermill any longer, notebook parameters no longer valid?
    #  kfp-notebook  has inputs and outputs ?
    parameters = dict()

    api_notebook = ApiNotebook(id=notebook_id,
                               created_at=created_at,
                               name=name,
                               description=description,
                               url=url,
                               metadata=metadata,
                               parameters=parameters,
                               filter_categories=filter_categories)

    uuid = store_data(api_notebook)

    api_notebook.id = uuid

    store_file(bucket_name="mlpipeline", prefix=f"notebooks/{notebook_id}/",
               file_name="template.yaml", file_content=yaml_file_content,
               content_type="text/yaml")

    s3_url = store_file(bucket_name="mlpipeline",
                        prefix=f"notebooks/{notebook_id}/",
                        file_name=url.split("/")[-1].split("?")[0],
                        file_content=json.dumps(notebook_content).encode())

    if requirements:

        if _is_url(requirements):
            requirements_url = requirements
            requirements_txt = download_file_content_from_url(requirements_url).decode()
        else:
            requirements_txt = "\n".join(requirements.split(","))

        # TODO: remove this after fixing the Elyra-AI/KFP-Notebook runner so that
        #   Elyra should install its own requirements in addition to the provided requirements
        requirements_elyra_url = "https://github.com/elyra-ai/kfp-notebook/blob/master/etc/requirements-elyra.txt"
        requirements_elyra_txt = download_file_content_from_url(requirements_elyra_url).decode()
        requirements_elyra = "\n".join([line for line in requirements_elyra_txt.split("\n")
                                        if not line.startswith("#")])

        requirements_all = f"# Required packages for {api_notebook.name}:\n" \
                           f"{requirements_txt}\n" \
                           f"# Requirements from {requirements_elyra_url}:\n" \
                           f"{requirements_elyra}"

        store_file(bucket_name="mlpipeline", prefix=f"notebooks/{notebook_id}/",
                   file_name="requirements.txt", file_content=requirements_all.encode())

    # if the url included an access token, replace the original url with the s3 url
    if "?token=" in url or "github.ibm.com" in url:
        api_notebook.url = s3_url
        update_multiple(ApiNotebook, [notebook_id], "url", s3_url)
        enable_anonymous_read_access(bucket_name="mlpipeline", prefix="notebooks/*")

    return api_notebook, 201


def _download_notebook(url: str, enterprise_github_api_token: str) -> dict:

    request_headers = dict()

    if "ibm.com" in url and "?token=" not in url:
        if not enterprise_github_api_token and not ghe_api_token:
            raise ApiError(f"Must provide API token to access notebooks on Enterprise GitHub: {url}", 422)
        else:
            request_headers.update({'Authorization': f'token {enterprise_github_api_token or ghe_api_token}'})

    try:
        raw_url = url.replace("/github.ibm.com/", "/raw.github.ibm.com/")\
                     .replace("/github.com/", "/raw.githubusercontent.com/")\
                     .replace("/blob/", "/")
        response = requests.get(raw_url, allow_redirects=True, headers=request_headers)

        if response.ok:
            notebook_dict = response.json()
            return notebook_dict

    except Exception as e:
        raise ApiError(f"Could not download notebook file '{url}'. \n{str(e)}", 422)

    raise ApiError(f"Could not download notebook file '{url}'. Reason: {response.reason}",
                   response.status_code)


def _extract_notebook_parameters(notebook_dict: dict) -> [ApiParameter]:
    """deprecated: was used to determine Papermill notebook parameters"""

    # try:
    #     parameters: [ApiParameter] = []
    #
    #     for cell in notebook_dict["cells"]:
    #         if "parameters" in cell["metadata"].get("tags", {}):
    #             for line in cell["source"]:
    #                 # match = re.match(r"(?P<variable_name>\w+) *= *(?P<variable_value>.+)", line)
    #                 match = re.match(r"(?P<var_name>\w+) *= *(?P<var_value>.+)(# *(?P<var_description>.+) *)?", line)
    #
    #                 if match:
    #                     var_decl = match.groupdict()
    #                     api_parameter = ApiParameter(name=var_decl.get("var_name"),
    #                                                  description=var_decl.get("var_description"),
    #                                                  default=var_decl.get("var_value").strip('"').strip("'"),
    #                                                  value=None)
    #                     parameters.append(api_parameter)
    #             break
    #
    #     return parameters
    #
    # except Exception as e:
    #     raise ApiError(str(e), 422)

    return []


def _is_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
