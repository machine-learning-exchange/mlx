# swagger_client.NotebookServiceApi

All URIs are relative to *http://localhost/apis/v1alpha1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**approve_notebooks_for_publishing**](NotebookServiceApi.md#approve_notebooks_for_publishing) | **POST** /notebooks/publish_approved | 
[**create_notebook**](NotebookServiceApi.md#create_notebook) | **POST** /notebooks | 
[**delete_notebook**](NotebookServiceApi.md#delete_notebook) | **DELETE** /notebooks/{id} | 
[**download_notebook_files**](NotebookServiceApi.md#download_notebook_files) | **GET** /notebooks/{id}/download | Returns the notebook artifacts compressed into a .tgz (.tar.gz) file.
[**generate_notebook_code**](NotebookServiceApi.md#generate_notebook_code) | **GET** /notebooks/{id}/generate_code | 
[**get_notebook**](NotebookServiceApi.md#get_notebook) | **GET** /notebooks/{id} | 
[**get_notebook_template**](NotebookServiceApi.md#get_notebook_template) | **GET** /notebooks/{id}/templates | 
[**list_notebooks**](NotebookServiceApi.md#list_notebooks) | **GET** /notebooks | 
[**run_notebook**](NotebookServiceApi.md#run_notebook) | **POST** /notebooks/{id}/run | 
[**set_featured_notebooks**](NotebookServiceApi.md#set_featured_notebooks) | **POST** /notebooks/featured | 
[**upload_notebook**](NotebookServiceApi.md#upload_notebook) | **POST** /notebooks/upload | 
[**upload_notebook_file**](NotebookServiceApi.md#upload_notebook_file) | **POST** /notebooks/{id}/upload | 
[**upload_notebook_from_url**](NotebookServiceApi.md#upload_notebook_from_url) | **POST** /notebooks/upload_from_url | 


# **approve_notebooks_for_publishing**
> approve_notebooks_for_publishing(notebook_ids)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.NotebookServiceApi()
notebook_ids = [swagger_client.list[str]()] # list[str] | Array of notebook IDs to be approved for publishing.

try:
    api_instance.approve_notebooks_for_publishing(notebook_ids)
except ApiException as e:
    print("Exception when calling NotebookServiceApi->approve_notebooks_for_publishing: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **notebook_ids** | **list[str]**| Array of notebook IDs to be approved for publishing. | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_notebook**
> ApiNotebook create_notebook(body)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.NotebookServiceApi()
body = swagger_client.ApiNotebook() # ApiNotebook | 

try:
    api_response = api_instance.create_notebook(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NotebookServiceApi->create_notebook: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ApiNotebook**](ApiNotebook.md)|  | 

### Return type

[**ApiNotebook**](ApiNotebook.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_notebook**
> delete_notebook(id)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.NotebookServiceApi()
id = 'id_example' # str | 

try:
    api_instance.delete_notebook(id)
except ApiException as e:
    print("Exception when calling NotebookServiceApi->delete_notebook: %s\n" % e)
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

# **download_notebook_files**
> file download_notebook_files(id, include_generated_code=include_generated_code)

Returns the notebook artifacts compressed into a .tgz (.tar.gz) file.

### Example
```python
from __future__ import print_function
import swagger_client
from swagger_client.rest import ApiException
from urllib3.response import HTTPResponse


# create an instance of the API class
api_instance = swagger_client.NotebookServiceApi()
notebook_id = 'ye-23fg0-2ic8' # str
include_generated_code = True # bool | Include generated run script in download (optional) (default to false)
tarfile_path = f'download/notebook_{notebook_id}.tgz'

try:
    # Returns the notebook artifacts compressed into a .tgz (.tar.gz) file.
    response: HTTPResponse = \
        api_instance.download_notebook_files(notebook_id,
                                             include_generated_code=include_generated_code,
                                             _preload_content=False)
    with open(tarfile_path, 'wb') as f:
        f.write(response.read())
except ApiException as e:
    print("Exception when calling NotebookServiceApi->download_notebook_files: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **include_generated_code** | **bool**| Include generated run script in download | [optional] [default to false]

### Return type

**file**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/gzip

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **generate_notebook_code**
> ApiGenerateCodeResponse generate_notebook_code(id)



Generate sample code to use notebook in a pipeline

### Example
```python
from __future__ import print_function
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.NotebookServiceApi()
id = 'id_example' # str | 

try:
    api_response = api_instance.generate_notebook_code(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NotebookServiceApi->generate_notebook_code: %s\n" % e)
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

# **get_notebook**
> ApiNotebook get_notebook(id)



### Example
```python
from __future__ import print_function
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.NotebookServiceApi()
id = 'id_example' # str | 

try:
    api_response = api_instance.get_notebook(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NotebookServiceApi->get_notebook: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**ApiNotebook**](ApiNotebook.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_notebook_template**
> ApiGetTemplateResponse get_notebook_template(id)



### Example
```python
from __future__ import print_function
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.NotebookServiceApi()
id = 'id_example' # str | 

try:
    api_response = api_instance.get_notebook_template(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NotebookServiceApi->get_notebook_template: %s\n" % e)
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

# **list_notebooks**
> ApiListNotebooksResponse list_notebooks(page_token=page_token, page_size=page_size, sort_by=sort_by, filter=filter)



### Example
```python
from __future__ import print_function
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.NotebookServiceApi()
page_token = 'page_token_example' # str |  (optional)
page_size = 56 # int |  (optional)
sort_by = 'name' # str | Can be format of \"field_name\", \"field_name asc\" or \"field_name desc\" Ascending by default. (optional)
filter = '{"name": "my notebook"}' # str | A string-serialized JSON dictionary with key-value pairs that correspond to the Notebook's attribute names and their respective values to be filtered for. (optional)

try:
    api_response = api_instance.list_notebooks(page_token=page_token, page_size=page_size, sort_by=sort_by, filter=filter)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NotebookServiceApi->list_notebooks: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page_token** | **str**|  | [optional] 
 **page_size** | **int**|  | [optional] 
 **sort_by** | **str**| Can be format of \&quot;field_name\&quot;, \&quot;field_name asc\&quot; or \&quot;field_name desc\&quot; Ascending by default. | [optional] 
 **filter** | **str**| A string-serialized JSON dictionary with key-value pairs that correspond to the Notebook&#39;s attribute names and their respective values to be filtered for. | [optional] 

### Return type

[**ApiListNotebooksResponse**](ApiListNotebooksResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **run_notebook**
> ApiRunCodeResponse run_notebook(id, run_name=run_name, parameters=parameters)



### Example
```python
from __future__ import print_function
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.NotebookServiceApi()
id = 'id_example' # str | 
run_name = 'run_name_example' # str | name to identify the run on the Kubeflow Pipelines UI, defaults to notebook name (optional)
parameters = dict() # dict | optional run parameters, may be required based on pipeline definition (optional)

try:
    api_response = api_instance.run_notebook(id, run_name=run_name, parameters=parameters)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NotebookServiceApi->run_notebook: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **run_name** | **str**| name to identify the run on the Kubeflow Pipelines UI, defaults to notebook name | [optional] 
 **parameters** | [**Dictionary**](Dictionary.md)| optional run parameters, may be required based on pipeline definition | [optional] 

### Return type

[**ApiRunCodeResponse**](ApiRunCodeResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_featured_notebooks**
> set_featured_notebooks(notebook_ids)



### Example
```python
from __future__ import print_function
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.NotebookServiceApi()
notebook_ids = [swagger_client.list[str]()] # list[str] | Array of notebook IDs to be featured.

try:
    api_instance.set_featured_notebooks(notebook_ids)
except ApiException as e:
    print("Exception when calling NotebookServiceApi->set_featured_notebooks: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **notebook_ids** | **list[str]**| Array of notebook IDs to be featured. | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_notebook**
> ApiNotebook upload_notebook(uploadfile, name=name, enterprise_github_token=enterprise_github_token)



### Example
```python
from __future__ import print_function
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.NotebookServiceApi()
uploadfile = '/path/to/file.txt' # file | The notebook metadata YAML file to upload. Can be a GZip-compressed TAR file (.tgz, .tar.gz) or a YAML file (.yaml, .yml). Maximum size is 32MB.
name = 'name_example' # str |  (optional)
enterprise_github_token = 'enterprise_github_token_example' # str | Optional GitHub API token providing read-access to notebooks stored on Enterprise GitHub accounts. (optional)

try:
    api_response = api_instance.upload_notebook(uploadfile, name=name, enterprise_github_token=enterprise_github_token)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NotebookServiceApi->upload_notebook: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uploadfile** | **file**| The notebook metadata YAML file to upload. Can be a GZip-compressed TAR file (.tgz, .tar.gz) or a YAML file (.yaml, .yml). Maximum size is 32MB. | 
 **name** | **str**|  | [optional] 
 **enterprise_github_token** | **str**| Optional GitHub API token providing read-access to notebooks stored on Enterprise GitHub accounts. | [optional] 

### Return type

[**ApiNotebook**](ApiNotebook.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_notebook_file**
> ApiNotebook upload_notebook_file(id, uploadfile)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.NotebookServiceApi()
id = 'id_example' # str | The id of the notebook.
uploadfile = '/path/to/file.txt' # file | The file to upload, overwriting existing. Can be a GZip-compressed TAR file (.tgz), a YAML file (.yaml), Python script (.py), or Markdown file (.md)

try:
    api_response = api_instance.upload_notebook_file(id, uploadfile)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NotebookServiceApi->upload_notebook_file: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The id of the notebook. | 
 **uploadfile** | **file**| The file to upload, overwriting existing. Can be a GZip-compressed TAR file (.tgz), a YAML file (.yaml), Python script (.py), or Markdown file (.md) | 

### Return type

[**ApiNotebook**](ApiNotebook.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_notebook_from_url**
> ApiNotebook upload_notebook_from_url(url, name=name, access_token=access_token)



### Example
```python
from __future__ import print_function
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.NotebookServiceApi()
url = 'url_example' # str | URL pointing to the notebook YAML file.
name = 'name_example' # str | Optional, the name of the notebook to be created overriding the name in the YAML file. (optional)
access_token = 'access_token_example' # str | Optional, the Bearer token to access the 'url'. (optional)

try:
    api_response = api_instance.upload_notebook_from_url(url, name=name, access_token=access_token)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NotebookServiceApi->upload_notebook_from_url: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **url** | **str**| URL pointing to the notebook YAML file. | 
 **name** | **str**| Optional, the name of the notebook to be created overriding the name in the YAML file. | [optional] 
 **access_token** | **str**| Optional, the Bearer token to access the &#39;url&#39;. | [optional] 

### Return type

[**ApiNotebook**](ApiNotebook.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

