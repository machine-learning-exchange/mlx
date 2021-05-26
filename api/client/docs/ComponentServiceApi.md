# swagger_client.ComponentServiceApi

All URIs are relative to *http://localhost/apis/v1alpha1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**approve_components_for_publishing**](ComponentServiceApi.md#approve_components_for_publishing) | **POST** /components/publish_approved | 
[**create_component**](ComponentServiceApi.md#create_component) | **POST** /components | 
[**delete_component**](ComponentServiceApi.md#delete_component) | **DELETE** /components/{id} | 
[**download_component_files**](ComponentServiceApi.md#download_component_files) | **GET** /components/{id}/download | Returns the component artifacts compressed into a .tgz (.tar.gz) file.
[**generate_component_code**](ComponentServiceApi.md#generate_component_code) | **GET** /components/{id}/generate_code | 
[**get_component**](ComponentServiceApi.md#get_component) | **GET** /components/{id} | 
[**get_component_template**](ComponentServiceApi.md#get_component_template) | **GET** /components/{id}/templates | 
[**list_components**](ComponentServiceApi.md#list_components) | **GET** /components | 
[**run_component**](ComponentServiceApi.md#run_component) | **POST** /components/{id}/run | 
[**set_featured_components**](ComponentServiceApi.md#set_featured_components) | **POST** /components/featured | 
[**upload_component**](ComponentServiceApi.md#upload_component) | **POST** /components/upload | 
[**upload_component_file**](ComponentServiceApi.md#upload_component_file) | **POST** /components/{id}/upload | 
[**upload_component_from_url**](ComponentServiceApi.md#upload_component_from_url) | **POST** /components/upload_from_url | 


# **approve_components_for_publishing**
> approve_components_for_publishing(component_ids)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ComponentServiceApi()
component_ids = [swagger_client.list[str]()] # list[str] | Array of component IDs to be approved for publishing.

try:
    api_instance.approve_components_for_publishing(component_ids)
except ApiException as e:
    print("Exception when calling ComponentServiceApi->approve_components_for_publishing: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **component_ids** | **list[str]**| Array of component IDs to be approved for publishing. | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_component**
> ApiComponent create_component(body)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ComponentServiceApi()
body = swagger_client.ApiComponent() # ApiComponent | 

try:
    api_response = api_instance.create_component(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ComponentServiceApi->create_component: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ApiComponent**](ApiComponent.md)|  | 

### Return type

[**ApiComponent**](ApiComponent.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_component**
> delete_component(id)



### Example
```python
from __future__ import print_function
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ComponentServiceApi()
id = 'id_example' # str | 

try:
    api_instance.delete_component(id)
except ApiException as e:
    print("Exception when calling ComponentServiceApi->delete_component: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **download_component_files**
> file download_component_files(id, include_generated_code=include_generated_code)

Returns the component artifacts compressed into a .tgz (.tar.gz) file.

### Example
```python
from __future__ import print_function
import swagger_client
from swagger_client.rest import ApiException
from urllib3.response import HTTPResponse


# create an instance of the API class
api_instance = swagger_client.ComponentServiceApi()
component_id = '3diutD-2nDPQ' # str
include_generated_code = True # bool | Include generated run script in download (optional) (default to false)
tarfile_path = f'download/component_{component_id}.tgz'

try:
    # Returns the component artifacts compressed into a .tgz (.tar.gz) file.
    response: HTTPResponse = \
        api_instance.download_component_files(component_id,
                                              include_generated_code=include_generated_code,
                                              _preload_content=False)
    with open(tarfile_path, 'wb') as f:
        f.write(response.read())
except ApiException as e:
    print("Exception when calling ComponentServiceApi->download_component_files: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| UUID of component |
 **include_generated_code** | **bool**| Include generated run script in download | [optional] [default to false]

### Return type

**file**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/gzip

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **generate_component_code**
> ApiGenerateCodeResponse generate_component_code(id)



Generate sample code to use component in a pipeline

### Example
```python
from __future__ import print_function
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ComponentServiceApi()
id = 'id_example' # str | 

try:
    api_response = api_instance.generate_component_code(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ComponentServiceApi->generate_component_code: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**ApiGenerateCodeResponse**](ApiGenerateCodeResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_component**
> ApiComponent get_component(id)



### Example
```python
from __future__ import print_function
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ComponentServiceApi()
id = 'id_example' # str | 

try:
    api_response = api_instance.get_component(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ComponentServiceApi->get_component: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**ApiComponent**](ApiComponent.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_component_template**
> ApiGetTemplateResponse get_component_template(id)



### Example
```python
from __future__ import print_function
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ComponentServiceApi()
id = 'id_example' # str | 

try:
    api_response = api_instance.get_component_template(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ComponentServiceApi->get_component_template: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**ApiGetTemplateResponse**](ApiGetTemplateResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_components**
> ApiListComponentsResponse list_components(page_token=page_token, page_size=page_size, sort_by=sort_by, filter=filter)



### Example
```python
from __future__ import print_function
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ComponentServiceApi()
page_token = 'page_token_example' # str |  (optional)
page_size = 56 # int |  (optional)
sort_by = 'name' # str | Can be format of \"field_name\", \"field_name asc\" or \"field_name desc\" Ascending by default. (optional)
filter = '{"name": "test"}' # str | A string-serialized JSON dictionary with key-value pairs that correspond to the ApiComponent's attribute names and their respective values to be filtered for. (optional)

try:
    api_response = api_instance.list_components(page_token=page_token, page_size=page_size, sort_by=sort_by, filter=filter)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ComponentServiceApi->list_components: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page_token** | **str**|  | [optional] 
 **page_size** | **int**|  | [optional] 
 **sort_by** | **str**| Can be format of \&quot;field_name\&quot;, \&quot;field_name asc\&quot; or \&quot;field_name desc\&quot; Ascending by default. | [optional] 
 **filter** | **str**| A string-serialized JSON dictionary with key-value pairs that correspond to the ApiComponent&#39;s attribute names and their respective values to be filtered for. | [optional] 

### Return type

[**ApiListComponentsResponse**](ApiListComponentsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **run_component**
> ApiRunCodeResponse run_component(id, parameters, run_name=run_name)



### Example
```python
from __future__ import print_function
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ComponentServiceApi()
id = 'id_example' # str | 
parameters = [swagger_client.ApiParameter()] # list[ApiParameter] | 
run_name = 'run_name_example' # str | name to identify the run on the Kubeflow Pipelines UI, defaults to component name (optional)

try:
    api_response = api_instance.run_component(id, parameters, run_name=run_name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ComponentServiceApi->run_component: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **parameters** | [**list[ApiParameter]**](ApiParameter.md)|  | 
 **run_name** | **str**| name to identify the run on the Kubeflow Pipelines UI, defaults to component name | [optional] 

### Return type

[**ApiRunCodeResponse**](ApiRunCodeResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_featured_components**
> set_featured_components(component_ids)



### Example
```python
from __future__ import print_function
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ComponentServiceApi()
component_ids = [swagger_client.list[str]()] # list[str] | Array of component IDs to be featured.

try:
    api_instance.set_featured_components(component_ids)
except ApiException as e:
    print("Exception when calling ComponentServiceApi->set_featured_components: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **component_ids** | **list[str]**| Array of component IDs to be featured. | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_component**
> ApiComponent upload_component(uploadfile, name=name)



### Example
```python
from __future__ import print_function
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ComponentServiceApi()
uploadfile = '/path/to/file.txt' # file | The component YAML file to upload. Can be a GZip-compressed TAR file (.tgz, .tar.gz) or a YAML file (.yaml, .yml). Maximum size is 32MB.
name = 'name_example' # str |  (optional)

try:
    api_response = api_instance.upload_component(uploadfile, name=name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ComponentServiceApi->upload_component: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uploadfile** | **file**| The component YAML file to upload. Can be a GZip-compressed TAR file (.tgz, .tar.gz) or a YAML file (.yaml, .yml). Maximum size is 32MB. | 
 **name** | **str**|  | [optional] 

### Return type

[**ApiComponent**](ApiComponent.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_component_file**
> ApiComponent upload_component_file(id, uploadfile)



### Example
```python
from __future__ import print_function
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ComponentServiceApi()
id = 'id_example' # str | The id of the component.
uploadfile = '/path/to/file.txt' # file | The file to upload, overwriting existing. Can be a GZip-compressed TAR file (.tgz), a YAML file (.yaml), Python script (.py), or Markdown file (.md)

try:
    api_response = api_instance.upload_component_file(id, uploadfile)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ComponentServiceApi->upload_component_file: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The id of the component. | 
 **uploadfile** | **file**| The file to upload, overwriting existing. Can be a GZip-compressed TAR file (.tgz), a YAML file (.yaml), Python script (.py), or Markdown file (.md) | 

### Return type

[**ApiComponent**](ApiComponent.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_component_from_url**
> ApiComponent upload_component_from_url(url, name=name, access_token=access_token)



### Example
```python
from __future__ import print_function
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ComponentServiceApi()
url = 'url_example' # str | URL pointing to the component YAML file.
name = 'name_example' # str | Optional, the name of the component to be created overriding the name in the YAML file. (optional)
access_token = 'access_token_example' # str | Optional, the Bearer token to access the 'url'. (optional)

try:
    api_response = api_instance.upload_component_from_url(url, name=name, access_token=access_token)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ComponentServiceApi->upload_component_from_url: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **url** | **str**| URL pointing to the component YAML file. | 
 **name** | **str**| Optional, the name of the component to be created overriding the name in the YAML file. | [optional] 
 **access_token** | **str**| Optional, the Bearer token to access the &#39;url&#39;. | [optional] 

### Return type

[**ApiComponent**](ApiComponent.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

