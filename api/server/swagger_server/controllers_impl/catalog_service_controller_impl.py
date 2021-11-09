# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0

import connexion
import traceback

from swagger_server.data_access.mysql_client import update_multiple

from swagger_server.models import ApiCatalogUpload, ApiCatalogUploadError
from swagger_server.models import ApiCatalogUploadResponse, ApiListCatalogItemsResponse
from swagger_server.models import ApiComponent, ApiDataset, ApiModel, ApiNotebook, ApiPipelineExtension

from swagger_server.controllers_impl.component_service_controller_impl import list_components, upload_component_from_url
from swagger_server.controllers_impl.dataset_service_controller_impl import list_datasets, upload_dataset_from_url
from swagger_server.controllers_impl.model_service_controller_impl import list_models, upload_model_from_url
from swagger_server.controllers_impl.notebook_service_controller_impl import list_notebooks, upload_notebook_from_url
from swagger_server.controllers_impl.pipeline_service_controller_impl import list_pipelines, upload_pipeline_from_url

from swagger_server.util import ApiError


def list_all_assets(page_token=None, page_size=None, sort_by=None, filter=None):  # noqa: E501
    """list_all_assets

    :param page_token: 
    :type page_token: str
    :param page_size: 
    :type page_size: int
    :param sort_by: Can be format of \&quot;field_name\&quot;, \&quot;field_name asc\&quot; or \&quot;field_name desc\&quot; Ascending by default.
    :type sort_by: str
    :param filter: A string-serialized JSON dictionary with key-value pairs that correspond to the ApiComponent&#39;s attribute names and their respective values to be filtered for.
    :type filter: str

    :rtype: ApiListCatalogItemsResponse
    """

    if page_size == 0:
        return {}, 204

    # TODO: do not mis-use page_token as MySQL result offset
    offset = int(page_token) if page_token and page_token.isdigit() else 0

    if page_size or page_token:
        print(f"WARNING: page_size and page_token are not implemented on {__file__}#list_all_assets()")

    list_methods = {
        "components": list_components,
        "datasets": list_datasets,
        "models": list_models,
        "notebooks": list_notebooks,
        "pipelines": list_pipelines
    }

    api_response = ApiListCatalogItemsResponse(
        components=[], datasets=[], models=[], notebooks=[], pipelines=[],
        total_size=0)

    for asset_type, list_method in list_methods.items():

        asset_list_response, status = list_method(filter=filter, sort_by=sort_by)

        if 200 <= status < 300:
            asset_list = asset_list_response.__getattribute__(asset_type)
            api_response.__getattribute__(asset_type).extend(asset_list)

            # TODO: return filtered size or total number of all assets
            # api_response.total_size += asset_list_response.total_size
            api_response.total_size += len(asset_list)

    return api_response, 200


def upload_multiple_assets(body: ApiCatalogUpload):  # noqa: E501
    """upload_multiple_assets

    :param body: 
    :type body: ApiCatalogUpload

    :rtype: ApiCatalogUploadResponse
    """
    if connexion.request.is_json:
        body = ApiCatalogUpload.from_dict(connexion.request.get_json())  # noqa: E501

    # TODO: parameterize `publish_all` and `feature_all` flags, maybe? Although
    #   uploading a whole catalog is an admin activity, who most likely wants to
    #   register a curated list of assets that are to be published and featured
    publish_all = True
    feature_all = True

    def get_access_token_for_url(url: str) -> str:
        for api_access_token in body.api_access_tokens or []:
            if api_access_token.url_host in url:
                return api_access_token.api_token
        return None

    upload_methods = {
        "components": upload_component_from_url,
        "datasets": upload_dataset_from_url,
        "models": upload_model_from_url,
        "notebooks": upload_notebook_from_url,
        "pipelines": upload_pipeline_from_url
    }

    api_response = ApiCatalogUploadResponse(
        components=[], datasets=[], models=[], notebooks=[], pipelines=[],
        total_created=0, errors=[], total_errors=0)

    for asset_type, upload_method in upload_methods.items():
        for asset in body.__getattribute__(asset_type) or []:
            try:
                api_object, status = upload_method(
                    url=asset.url, name=asset.name,
                    access_token=get_access_token_for_url(asset.url))
                if 200 <= status < 300:
                    api_response.__getattribute__(asset_type).append(api_object)
                    api_response.total_created += 1
                else:
                    # TODO: remove this?
                    api_error = ApiCatalogUploadError(**asset.to_dict(),
                                                      error_message=f"THIS SHOULD NOT HAPPEN: {str(api_object).strip()}",
                                                      status_code=500)
                    api_response.errors.append(api_error)
                    print(f"THIS SHOULD NOT HAPPEN: {api_error}")
                    print(traceback.format_exc())

            except ApiError as e:
                api_error = ApiCatalogUploadError(**asset.to_dict(),
                                                  error_message=e.message,
                                                  status_code=e.http_status_code)
                api_response.errors.append(api_error)

            except Exception as e:
                api_error = ApiCatalogUploadError(**asset.to_dict(),
                                                  error_message=str(e),
                                                  status_code=500)
                api_response.errors.append(api_error)
                print(traceback.format_exc())

    api_response.total_errors = len(api_response.errors)

    if publish_all or feature_all:
        api_classes = {
            "components": ApiComponent,
            "datasets": ApiDataset,
            "models": ApiModel,
            "notebooks": ApiNotebook,
            "pipelines": ApiPipelineExtension
        }
        for asset_type, api_class in api_classes.items():
            asset_list = api_response.__getattribute__(asset_type)
            asset_ids = [asset.id for asset in asset_list]
            update_multiple(api_class, asset_ids, "publish_approved", publish_all)
            update_multiple(api_class, asset_ids, "featured", feature_all)

    response_status = \
        201 if api_response.total_created > 0 and api_response.total_errors == 0 else \
        207 if api_response.total_created > 0 and api_response.total_errors > 0 else \
        max([e.status_code for e in api_response.errors])

    return api_response, response_status
