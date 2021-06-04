# swagger_client.ModelServiceApi

All URIs are relative to *http://localhost/apis/v1alpha1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**approve_models_for_publishing**](ModelServiceApi.md#approve_models_for_publishing) | **POST** /models/publish_approved | 
[**create_model**](ModelServiceApi.md#create_model) | **POST** /models | 
[**delete_model**](ModelServiceApi.md#delete_model) | **DELETE** /models/{id} | 
[**download_model_files**](ModelServiceApi.md#download_model_files) | **GET** /models/{id}/download | Returns the model artifacts compressed into a .tgz (.tar.gz) file.
[**generate_model_code**](ModelServiceApi.md#generate_model_code) | **GET** /models/{id}/generate_code | 
[**get_model**](ModelServiceApi.md#get_model) | **GET** /models/{id} | 
[**get_model_template**](ModelServiceApi.md#get_model_template) | **GET** /models/{id}/templates | 
[**list_models**](ModelServiceApi.md#list_models) | **GET** /models | 
[**run_model**](ModelServiceApi.md#run_model) | **POST** /models/{id}/run | 
[**set_featured_models**](ModelServiceApi.md#set_featured_models) | **POST** /models/featured | 
[**upload_model**](ModelServiceApi.md#upload_model) | **POST** /models/upload | 
[**upload_model_file**](ModelServiceApi.md#upload_model_file) | **POST** /models/{id}/upload | 
[**upload_model_from_url**](ModelServiceApi.md#upload_model_from_url) | **POST** /models/upload_from_url | 


# **approve_models_for_publishing**
> approve_models_for_publishing(model_ids)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ModelServiceApi()
model_ids = [swagger_client.list[str]()] # list[str] | Array of model IDs to be approved for publishing.

try:
    api_instance.approve_models_for_publishing(model_ids)
except ApiException as e:
    print("Exception when calling ModelServiceApi->approve_models_for_publishing: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **model_ids** | **list[str]**| Array of model IDs to be approved for publishing. | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_model**
> ApiModel create_model(body)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ModelServiceApi()
body = swagger_client.ApiModel() # ApiModel | 

try:
    api_response = api_instance.create_model(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelServiceApi->create_model: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ApiModel**](ApiModel.md)|  | 

### Return type

[**ApiModel**](ApiModel.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_model**
> delete_model(id)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ModelServiceApi()
id = 'id_example' # str | 

try:
    api_instance.delete_model(id)
except ApiException as e:
    print("Exception when calling ModelServiceApi->delete_model: %s\n" % e)
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

# **download_model_files**
> file download_model_files(id, include_generated_code=include_generated_code)

Returns the model artifacts compressed into a .tgz (.tar.gz) file.

### Example
```python
from __future__ import print_function
import swagger_client
from swagger_client.rest import ApiException
from urllib3.response import HTTPResponse


# create an instance of the API class
api_instance = swagger_client.ModelServiceApi()
model_id = 'max-audio-classifier'  # str
include_generated_code = True  # bool | Include generated run scripts in download (optional) (default to false)
tarfile_path = f'download/{model_id}.tgz'

try:
    # Returns the model artifacts compressed into a .tgz (.tag.gz) file.
    response: HTTPResponse = \
        api_instance.download_model_files(model_id,
                                          include_generated_code=include_generated_code,
                                          _preload_content=False)
    with open(tarfile_path, 'wb') as f:
        f.write(response.read())
except ApiException as e:
    print("Exception when calling ModelServiceApi->download_model_files: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **include_generated_code** | **bool**| Include generated run scripts in download | [optional] [default to false]

### Return type

**file**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/gzip

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **generate_model_code**
> ApiGenerateModelCodeResponse generate_model_code(id)



### Example
```python
from __future__ import print_function
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ModelServiceApi()
id = 'id_example' # str | 

try:
    api_response = api_instance.generate_model_code(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelServiceApi->generate_model_code: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**ApiGenerateModelCodeResponse**](ApiGenerateModelCodeResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_model**
> ApiModel get_model(id)



### Example
```python
from __future__ import print_function
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ModelServiceApi()
id = 'id_example' # str | 

try:
    api_response = api_instance.get_model(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelServiceApi->get_model: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**ApiModel**](ApiModel.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_model_template**
> ApiGetTemplateResponse get_model_template(id)



### Example
```python
from __future__ import print_function
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ModelServiceApi()
id = 'id_example' # str | 

try:
    api_response = api_instance.get_model_template(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelServiceApi->get_model_template: %s\n" % e)
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

# **list_models**
> ApiListModelsResponse list_models(page_token=page_token, page_size=page_size, sort_by=sort_by, filter=filter)



### Example
```python
from __future__ import print_function
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ModelServiceApi()
page_token = 'page_token_example' # str |  (optional)
page_size = 56 # int |  (optional)
sort_by = 'name' # str | Can be format of \"field_name\", \"field_name asc\" or \"field_name desc\" Ascending by default. (optional)
filter = '{"name": "test"}' # str | A string-serialized JSON dictionary with key-value pairs that correspond to the Model's attribute names and their respective values to be filtered for. (optional)

try:
    api_response = api_instance.list_models(page_token=page_token, page_size=page_size, sort_by=sort_by, filter=filter)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelServiceApi->list_models: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page_token** | **str**|  | [optional] 
 **page_size** | **int**|  | [optional] 
 **sort_by** | **str**| Can be format of \&quot;field_name\&quot;, \&quot;field_name asc\&quot; or \&quot;field_name desc\&quot; Ascending by default. | [optional] 
 **filter** | **str**| A string-serialized JSON dictionary with key-value pairs that correspond to the Model&#39;s attribute names and their respective values to be filtered for. | [optional] 

### Return type

[**ApiListModelsResponse**](ApiListModelsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **run_model**
> ApiRunCodeResponse run_model(id, pipeline_stage, execution_platform, run_name=run_name, parameters=parameters)



### Example
```python
from __future__ import print_function
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ModelServiceApi()
id = 'id_example' # str | 
pipeline_stage = 'pipeline_stage_example' # str | pipeline stage, either 'train' or 'serve'
execution_platform = 'execution_platform_example' # str | execution platform, i.e. 'kubernetes', 'knative'
run_name = 'run_name_example' # str | name to identify the run on the Kubeflow Pipelines UI, defaults to model identifier (optional)
parameters = swagger_client.Dictionary() # Dictionary | optional run parameters, must include 'github_url' and 'github_token' if credentials are required (optional)

try:
    api_response = api_instance.run_model(id, pipeline_stage, execution_platform, run_name=run_name, parameters=parameters)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelServiceApi->run_model: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **pipeline_stage** | **str**| pipeline stage, either &#39;train&#39; or &#39;serve&#39; | 
 **execution_platform** | **str**| execution platform, i.e. &#39;kubernetes&#39;, &#39;knative&#39; | 
 **run_name** | **str**| name to identify the run on the Kubeflow Pipelines UI, defaults to model identifier | [optional] 
 **parameters** | [**Dictionary**](Dictionary.md)| optional run parameters, must include &#39;github_url&#39; and &#39;github_token&#39; if credentials are required | [optional] 

### Return type

[**ApiRunCodeResponse**](ApiRunCodeResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_featured_models**
> set_featured_models(model_ids)



### Example
```python
from __future__ import print_function
import swagger_client
from swagger_client.rest import ApiException

# create an instance of the API class
api_instance = swagger_client.ModelServiceApi()
model_ids = [swagger_client.list[str]()] # list[str] | Array of model IDs to be featured.

try:
    api_instance.set_featured_models(model_ids)
except ApiException as e:
    print("Exception when calling ModelServiceApi->set_featured_models: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **model_ids** | **list[str]**| Array of model IDs to be featured. | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_model**
> ApiModel upload_model(uploadfile, name=name)



### Example
```python
from __future__ import print_function
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ModelServiceApi()
uploadfile = '/path/to/file.txt' # file | The model YAML file to upload. Can be a GZip-compressed TAR file (.tgz, .tar.gz) or a YAML file (.yaml, .yml). Maximum size is 32MB.
name = 'my model' # str |  (optional)

try:
    api_response = api_instance.upload_model(uploadfile, name=name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelServiceApi->upload_model: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uploadfile** | **file**| The model YAML file to upload. Can be a GZip-compressed TAR file (.tgz, .tar.gz) or a YAML file (.yaml, .yml). Maximum size is 32MB. | 
 **name** | **str**|  | [optional] 

### Return type

[**ApiModel**](ApiModel.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_model_file**
> ApiModel upload_model_file(id, uploadfile)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ModelServiceApi()
id = 'id_example' # str | The model identifier.
uploadfile = '/path/to/file.txt' # file | The file to upload, overwriting existing. Can be a GZip-compressed TAR file (.tgz), a YAML file (.yaml), Python script (.py), or Markdown file (.md)

try:
    api_response = api_instance.upload_model_file(id, uploadfile)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelServiceApi->upload_model_file: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The model identifier. | 
 **uploadfile** | **file**| The file to upload, overwriting existing. Can be a GZip-compressed TAR file (.tgz), a YAML file (.yaml), Python script (.py), or Markdown file (.md) | 

### Return type

[**ApiModel**](ApiModel.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_model_from_url**
> ApiModel upload_model_from_url(url, name=name, access_token=access_token)



### Example
```python
from __future__ import print_function
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.ModelServiceApi()
url = 'url_example' # str | URL pointing to the model YAML file.
name = 'name_example' # str | Optional, the name of the model to be created overriding the name in the YAML file. (optional)
access_token = 'access_token_example' # str | Optional, the Bearer token to access the 'url'. (optional)

try:
    api_response = api_instance.upload_model_from_url(url, name=name, access_token=access_token)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelServiceApi->upload_model_from_url: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **url** | **str**| URL pointing to the model YAML file. | 
 **name** | **str**| Optional, the name of the model to be created overriding the name in the YAML file. | [optional] 
 **access_token** | **str**| Optional, the Bearer token to access the &#39;url&#39;. | [optional] 

### Return type

[**ApiModel**](ApiModel.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

