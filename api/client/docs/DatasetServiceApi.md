# swagger_client.DatasetServiceApi

All URIs are relative to *http://localhost/apis/v1alpha1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**approve_datasets_for_publishing**](DatasetServiceApi.md#approve_datasets_for_publishing) | **POST** /datasets/publish_approved | 
[**create_dataset**](DatasetServiceApi.md#create_dataset) | **POST** /datasets | 
[**delete_dataset**](DatasetServiceApi.md#delete_dataset) | **DELETE** /datasets/{id} | 
[**download_dataset_files**](DatasetServiceApi.md#download_dataset_files) | **GET** /datasets/{id}/download | Returns the dataset artifacts compressed into a .tgz (.tar.gz) file.
[**generate_dataset_code**](DatasetServiceApi.md#generate_dataset_code) | **GET** /datasets/{id}/generate_code | 
[**get_dataset**](DatasetServiceApi.md#get_dataset) | **GET** /datasets/{id} | 
[**get_dataset_template**](DatasetServiceApi.md#get_dataset_template) | **GET** /datasets/{id}/templates | 
[**list_datasets**](DatasetServiceApi.md#list_datasets) | **GET** /datasets | 
[**run_dataset**](DatasetServiceApi.md#run_dataset) | **POST** /datasets/{id}/run | 
[**set_featured_datasets**](DatasetServiceApi.md#set_featured_datasets) | **POST** /datasets/featured | 
[**upload_dataset**](DatasetServiceApi.md#upload_dataset) | **POST** /datasets/upload | 
[**upload_dataset_file**](DatasetServiceApi.md#upload_dataset_file) | **POST** /datasets/{id}/upload | 
[**upload_dataset_from_url**](DatasetServiceApi.md#upload_dataset_from_url) | **POST** /datasets/upload_from_url | 


# **approve_datasets_for_publishing**
> approve_datasets_for_publishing(dataset_ids)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException

# create an instance of the API class
api_instance = swagger_client.DatasetServiceApi()
dataset_ids = [swagger_client.list[str]()] # list[str] | Array of dataset IDs to be approved for publishing.

try:
    api_instance.approve_datasets_for_publishing(dataset_ids)
except ApiException as e:
    print("Exception when calling DatasetServiceApi->approve_datasets_for_publishing: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_ids** | **list[str]**| Array of dataset IDs to be approved for publishing. | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_dataset**
> ApiDataset create_dataset(body)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DatasetServiceApi()
body = swagger_client.ApiDataset() # ApiDataset | 

try:
    api_response = api_instance.create_dataset(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetServiceApi->create_dataset: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ApiDataset**](ApiDataset.md)|  | 

### Return type

[**ApiDataset**](ApiDataset.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_dataset**
> delete_dataset(id)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException

# create an instance of the API class
api_instance = swagger_client.DatasetServiceApi()
id = 'id_example' # str | 

try:
    api_instance.delete_dataset(id)
except ApiException as e:
    print("Exception when calling DatasetServiceApi->delete_dataset: %s\n" % e)
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

# **download_dataset_files**
> file download_dataset_files(id, include_generated_code=include_generated_code)

Returns the dataset artifacts compressed into a .tgz (.tar.gz) file.

### Example
```python
import swagger_client
from swagger_client.rest import ApiException
from urllib3.response import HTTPResponse

# create an instance of the API class
api_instance = swagger_client.DatasetServiceApi()
dataset_id = 'aetr91-aui3vc'
include_generated_code = True # include generated pipeline DSL script in download file (optional, default: False)
tarfile_path = f'download/dataset_{dataset_id}.tgz'

try:
    # Returns the dataset artifacts compressed into a .tgz (.tar.gz) file.
    response: HTTPResponse = api_instance.\
        download_dataset_files(dataset_id,
                               include_generated_code=include_generated_code,
                               __preload_content=False)
    with open(tarfile_path, 'wb') as f:
        f.write(response.read())
except ApiException as e:
    print("Exception when calling DatasetServiceApi->download_dataset_files: %s\n" % e)
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

# **generate_dataset_code**
> ApiGenerateCodeResponse generate_dataset_code(id)



Generate sample code to use dataset in a pipeline

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DatasetServiceApi()
id = 'id_example' # str | 

try:
    api_response = api_instance.generate_dataset_code(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetServiceApi->generate_dataset_code: %s\n" % e)
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

# **get_dataset**
> ApiDataset get_dataset(id)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DatasetServiceApi()
id = 'id_example' # str | 

try:
    api_response = api_instance.get_dataset(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetServiceApi->get_dataset: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**ApiDataset**](ApiDataset.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_dataset_template**
> ApiGetTemplateResponse get_dataset_template(id)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DatasetServiceApi()
id = 'id_example' # str | 

try:
    api_response = api_instance.get_dataset_template(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetServiceApi->get_dataset_template: %s\n" % e)
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

# **list_datasets**
> ApiListDatasetsResponse list_datasets(page_token=page_token, page_size=page_size, sort_by=sort_by, filter=filter)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DatasetServiceApi()
page_token = 'page_token_example' # str |  (optional)
page_size = 56 # int |  (optional)
sort_by = 'sort_by_example' # str | Can be format of 'field_name', 'field_name asc' or 'field_name desc'. Ascending by default. (optional)
filter = 'filter_example' # str | A string-serialized JSON dictionary containing key-value pairs with name of the object property to apply filter on and the value of the respective property. (optional)

try:
    api_response = api_instance.list_datasets(page_token=page_token, page_size=page_size, sort_by=sort_by, filter=filter)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetServiceApi->list_datasets: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page_token** | **str**|  | [optional] 
 **page_size** | **int**|  | [optional] 
 **sort_by** | **str**| Can be format of &#39;field_name&#39;, &#39;field_name asc&#39; or &#39;field_name desc&#39;. Ascending by default. | [optional] 
 **filter** | **str**| A string-serialized JSON dictionary containing key-value pairs with name of the object property to apply filter on and the value of the respective property. | [optional] 

### Return type

[**ApiListDatasetsResponse**](ApiListDatasetsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **run_dataset**
> ApiRunCodeResponse run_dataset(id, parameters=parameters, run_name=run_name)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DatasetServiceApi()
id = 'id_example' # str | 
parameters = [swagger_client.ApiParameter()] # list[ApiParameter] |  (optional)
run_name = 'run_name_example' # str | name to identify the run on the Kubeflow Pipelines UI, defaults to component name (optional)

try:
    api_response = api_instance.run_dataset(id, parameters=parameters, run_name=run_name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetServiceApi->run_dataset: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **parameters** | [**list[ApiParameter]**](ApiParameter.md)|  | [optional] 
 **run_name** | **str**| name to identify the run on the Kubeflow Pipelines UI, defaults to component name | [optional] 

### Return type

[**ApiRunCodeResponse**](ApiRunCodeResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_featured_datasets**
> set_featured_datasets(dataset_ids)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DatasetServiceApi()
dataset_ids = [swagger_client.list[str]()] # list[str] | Array of dataset IDs to be featured.

try:
    api_instance.set_featured_datasets(dataset_ids)
except ApiException as e:
    print("Exception when calling DatasetServiceApi->set_featured_datasets: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_ids** | **list[str]**| Array of dataset IDs to be featured. | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_dataset**
> ApiDataset upload_dataset(uploadfile, name=name)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DatasetServiceApi()
uploadfile = '/path/to/file.txt' # file | The dataset YAML file to upload. Can be a GZip-compressed TAR file (.tgz, .tar.gz) or a YAML file (.yaml, .yml). Maximum size is 32MB.
name = 'name_example' # str |  (optional)

try:
    api_response = api_instance.upload_dataset(uploadfile, name=name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetServiceApi->upload_dataset: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uploadfile** | **file**| The dataset YAML file to upload. Can be a GZip-compressed TAR file (.tgz, .tar.gz) or a YAML file (.yaml, .yml). Maximum size is 32MB. | 
 **name** | **str**|  | [optional] 

### Return type

[**ApiDataset**](ApiDataset.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_dataset_file**
> ApiDataset upload_dataset_file(id, uploadfile)



### Example
```python
from __future__ import print_function
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DatasetServiceApi()
id = 'id_example' # str | The id of the dataset.
uploadfile = '/path/to/file.txt' # file | The file to upload, overwriting existing. Can be a GZip-compressed TAR file (.tgz), a YAML file (.yaml), Python script (.py), or Markdown file (.md)

try:
    api_response = api_instance.upload_dataset_file(id, uploadfile)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetServiceApi->upload_dataset_file: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The id of the dataset. | 
 **uploadfile** | **file**| The file to upload, overwriting existing. Can be a GZip-compressed TAR file (.tgz), a YAML file (.yaml), Python script (.py), or Markdown file (.md) | 

### Return type

[**ApiDataset**](ApiDataset.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_dataset_from_url**
> ApiDataset upload_dataset_from_url(url, name=name, access_token=access_token)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DatasetServiceApi()
url = 'url_example' # str | URL pointing to the dataset YAML file.
name = 'name_example' # str | Optional, the name of the dataset to be created overriding the name in the YAML file. (optional)
access_token = 'access_token_example' # str | Optional, the Bearer token to access the 'url'. (optional)

try:
    api_response = api_instance.upload_dataset_from_url(url, name=name, access_token=access_token)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DatasetServiceApi->upload_dataset_from_url: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **url** | **str**| URL pointing to the dataset YAML file. | 
 **name** | **str**| Optional, the name of the dataset to be created overriding the name in the YAML file. | [optional] 
 **access_token** | **str**| Optional, the Bearer token to access the &#39;url&#39;. | [optional] 

### Return type

[**ApiDataset**](ApiDataset.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

