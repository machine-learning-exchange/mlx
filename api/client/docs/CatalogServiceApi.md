# swagger_client.CatalogServiceApi

All URIs are relative to *http://localhost/apis/v1alpha1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**list_all_assets**](CatalogServiceApi.md#list_all_assets) | **GET** /catalog | 
[**upload_multiple_assets**](CatalogServiceApi.md#upload_multiple_assets) | **POST** /catalog | 


# **list_all_assets**
> ApiListCatalogItemsResponse list_all_assets(page_token=page_token, page_size=page_size, sort_by=sort_by, filter=filter)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.CatalogServiceApi()
page_token = 'page_token_example' # str |  (optional)
page_size = 56 # int |  (optional)
sort_by = 'sort_by_example' # str | Can be format of \"field_name\", \"field_name asc\" or \"field_name desc\" Ascending by default. (optional)
filter = 'filter_example' # str | A string-serialized JSON dictionary with key-value pairs that correspond to the ApiComponent's attribute names and their respective values to be filtered for. (optional)

try:
    api_response = api_instance.list_all_assets(page_token=page_token, page_size=page_size, sort_by=sort_by, filter=filter)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CatalogServiceApi->list_all_assets: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page_token** | **str**|  | [optional] 
 **page_size** | **int**|  | [optional] 
 **sort_by** | **str**| Can be format of \&quot;field_name\&quot;, \&quot;field_name asc\&quot; or \&quot;field_name desc\&quot; Ascending by default. | [optional] 
 **filter** | **str**| A string-serialized JSON dictionary with key-value pairs that correspond to the ApiComponent&#39;s attribute names and their respective values to be filtered for. | [optional] 

### Return type

[**ApiListCatalogItemsResponse**](ApiListCatalogItemsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_multiple_assets**
> ApiCatalogUploadResponse upload_multiple_assets(body)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.CatalogServiceApi()
body = swagger_client.ApiCatalogUpload() # ApiCatalogUpload | 

try:
    api_response = api_instance.upload_multiple_assets(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CatalogServiceApi->upload_multiple_assets: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ApiCatalogUpload**](ApiCatalogUpload.md)|  | 

### Return type

[**ApiCatalogUploadResponse**](ApiCatalogUploadResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

