# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0

from swagger_server.models.api_catalog_upload import ApiCatalogUpload  # noqa: F401, E501
from swagger_server.models.api_catalog_upload_response import (  # noqa: F401
    ApiCatalogUploadResponse,
)
from swagger_server.models.api_list_catalog_items_response import (  # noqa: F401
    ApiListCatalogItemsResponse,
)
from swagger_server import util  # noqa: F401


def list_all_assets(
    page_token=None, page_size=None, sort_by=None, filter=None
):  # noqa: E501
    """list_all_assets

     # noqa: E501

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
    return util.invoke_controller_impl()


def upload_catalog_from_url(url, access_token=None):  # noqa: E501
    """upload_catalog_from_url

     # noqa: E501

    :param url: URL pointing to the catalog YAML file.
    :type url: str
    :param access_token: Optional, the Bearer token to access the &#39;url&#39;.
    :type access_token: str

    :rtype: ApiCatalogUploadResponse
    """
    return util.invoke_controller_impl()


def upload_multiple_assets(body):  # noqa: E501
    """upload_multiple_assets

     # noqa: E501

    :param body:
    :type body: ApiCatalogUpload

    :rtype: ApiCatalogUploadResponse
    """
    return util.invoke_controller_impl()
