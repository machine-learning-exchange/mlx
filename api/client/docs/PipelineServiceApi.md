# swagger_client.PipelineServiceApi

All URIs are relative to *http://localhost/apis/v1alpha1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**approve_pipelines_for_publishing**](PipelineServiceApi.md#approve_pipelines_for_publishing) | **POST** /pipelines/publish_approved | 
[**create_pipeline**](PipelineServiceApi.md#create_pipeline) | **POST** /pipelines | 
[**delete_pipeline**](PipelineServiceApi.md#delete_pipeline) | **DELETE** /pipelines/{id} | 
[**download_pipeline_files**](PipelineServiceApi.md#download_pipeline_files) | **GET** /pipelines/{id}/download | Returns the pipeline YAML compressed into a .tgz (.tar.gz) file.
[**get_pipeline**](PipelineServiceApi.md#get_pipeline) | **GET** /pipelines/{id} | 
[**get_template**](PipelineServiceApi.md#get_template) | **GET** /pipelines/{id}/templates | 
[**list_pipelines**](PipelineServiceApi.md#list_pipelines) | **GET** /pipelines | 
[**run_custom_pipeline**](PipelineServiceApi.md#run_custom_pipeline) | **POST** /pipelines/run_custom_pipeline | 
[**run_pipeline**](PipelineServiceApi.md#run_pipeline) | **POST** /pipelines/{id}/run | 
[**set_featured_pipelines**](PipelineServiceApi.md#set_featured_pipelines) | **POST** /pipelines/featured | 
[**upload_pipeline**](PipelineServiceApi.md#upload_pipeline) | **POST** /pipelines/upload | 
[**upload_pipeline_from_url**](PipelineServiceApi.md#upload_pipeline_from_url) | **POST** /pipelines/upload_from_url | 


# **approve_pipelines_for_publishing**
> approve_pipelines_for_publishing(pipeline_ids)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PipelineServiceApi()
pipeline_ids = [swagger_client.list[str]()] # list[str] | Array of pipeline IDs to be approved for publishing.

try:
    api_instance.approve_pipelines_for_publishing(pipeline_ids)
except ApiException as e:
    print("Exception when calling PipelineServiceApi->approve_pipelines_for_publishing: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pipeline_ids** | **list[str]**| Array of pipeline IDs to be approved for publishing. | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_pipeline**
> ApiPipeline create_pipeline(body)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PipelineServiceApi()
body = swagger_client.ApiPipeline() # ApiPipeline | 

try:
    api_response = api_instance.create_pipeline(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PipelineServiceApi->create_pipeline: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ApiPipeline**](ApiPipeline.md)|  | 

### Return type

[**ApiPipeline**](ApiPipeline.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_pipeline**
> delete_pipeline(id)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException

# create an instance of the API class
api_instance = swagger_client.PipelineServiceApi()
id = 'id_example' # str | 

try:
    api_instance.delete_pipeline(id)
except ApiException as e:
    print("Exception when calling PipelineServiceApi->delete_pipeline: %s\n" % e)
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

# **download_pipeline_files**
> file download_pipeline_files(id)

Returns the pipeline YAML compressed into a .tgz (.tar.gz) file.

### Example
```python
from __future__ import print_function
import swagger_client
from swagger_client.rest import ApiException
from urllib3.response import HTTPResponse


# create an instance of the API class
api_instance = swagger_client.PipelineServiceApi()
id = 'wer32ia-de14n2-rDN1e34'
tarfile_path = f'download/pipeline_{id}.tgz'

try:
    # Returns the pipeline YAML compressed into a .tgz (.tar.gz) file.
    response: HTTPResponse = \
        api_instance.download_pipeline_files(id, _preload_content=False)
    with open(tarfile_path, 'wb') as f:
        f.write(response.read())
except ApiException as e:
    print("Exception when calling PipelineServiceApi->download_pipeline_files: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

**file**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/gzip

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_pipeline**
> ApiPipelineExtended get_pipeline(id)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PipelineServiceApi()
id = 'id_example' # str | 

try:
    api_response = api_instance.get_pipeline(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PipelineServiceApi->get_pipeline: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**ApiPipelineExtended**](ApiPipelineExtended.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_template**
> ApiGetTemplateResponse get_template(id)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PipelineServiceApi()
id = 'id_example' # str | 

try:
    api_response = api_instance.get_template(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PipelineServiceApi->get_template: %s\n" % e)
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

# **list_pipelines**
> ApiListPipelinesResponse list_pipelines(page_token=page_token, page_size=page_size, sort_by=sort_by, filter=filter)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PipelineServiceApi()
page_token = 'page_token_example' # str |  (optional)
page_size = 56 # int |  (optional)
sort_by = 'name' # str | Can be format of \"field_name\", \"field_name asc\" or \"field_name desc\" Ascending by default. (optional)
filter = '{"name": "my pipeline"}' # str | A string-serialized JSON dictionary with key-value pairs that correspond to the Pipeline's attribute names and their respective values to be filtered for. (optional)

try:
    api_response = api_instance.list_pipelines(page_token=page_token, page_size=page_size, sort_by=sort_by, filter=filter)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PipelineServiceApi->list_pipelines: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page_token** | **str**|  | [optional] 
 **page_size** | **int**|  | [optional] 
 **sort_by** | **str**| Can be format of \&quot;field_name\&quot;, \&quot;field_name asc\&quot; or \&quot;field_name desc\&quot; Ascending by default. | [optional] 
 **filter** | **str**| A string-serialized JSON dictionary with key-value pairs that correspond to the Pipeline&#39;s attribute names and their respective values to be filtered for. | [optional] 

### Return type

[**ApiListPipelinesResponse**](ApiListPipelinesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **run_custom_pipeline**
> ApiRunCodeResponse run_custom_pipeline(run_custom_pipeline_payload, run_name=run_name)



Run a complex pipeline defined by a directed acyclic graph (DAG)

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PipelineServiceApi()
run_custom_pipeline_payload = swagger_client.ApiPipelineCustomRunPayload() # ApiPipelineCustomRunPayload | A custom pipeline defined by a directed acyclic graph (DAG) and input parameters
run_name = 'run_name_example' # str | Name to identify the run on the Kubeflow Pipelines UI (optional)

try:
    api_response = api_instance.run_custom_pipeline(run_custom_pipeline_payload, run_name=run_name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PipelineServiceApi->run_custom_pipeline: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **run_custom_pipeline_payload** | [**ApiPipelineCustomRunPayload**](ApiPipelineCustomRunPayload.md)| A custom pipeline defined by a directed acyclic graph (DAG) and input parameters | 
 **run_name** | **str**| Name to identify the run on the Kubeflow Pipelines UI | [optional] 

### Return type

[**ApiRunCodeResponse**](ApiRunCodeResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **run_pipeline**
> ApiRunCodeResponse run_pipeline(id, run_name=run_name, parameters=parameters)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PipelineServiceApi()
id = 'id_example' # str | 
run_name = 'run_name_example' # str | name to identify the run on the Kubeflow Pipelines UI, defaults to pipeline name (optional)
parameters = swagger_client.Dictionary() # Dictionary | optional run parameters, may be required based on pipeline definition (optional)

try:
    api_response = api_instance.run_pipeline(id, run_name=run_name, parameters=parameters)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PipelineServiceApi->run_pipeline: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **run_name** | **str**| name to identify the run on the Kubeflow Pipelines UI, defaults to pipeline name | [optional] 
 **parameters** | [**Dictionary**](Dictionary.md)| optional run parameters, may be required based on pipeline definition | [optional] 

### Return type

[**ApiRunCodeResponse**](ApiRunCodeResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_featured_pipelines**
> set_featured_pipelines(pipeline_ids)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PipelineServiceApi()
pipeline_ids = [swagger_client.list[str]()] # list[str] | Array of pipeline IDs to be featured.

try:
    api_instance.set_featured_pipelines(pipeline_ids)
except ApiException as e:
    print("Exception when calling PipelineServiceApi->set_featured_pipelines: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pipeline_ids** | **list[str]**| Array of pipeline IDs to be featured. | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_pipeline**
> ApiPipelineExtended upload_pipeline(uploadfile, name=name, description=description, annotations=annotations)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PipelineServiceApi()
uploadfile = '/path/to/file.txt' # file | The pipeline YAML file to upload. Can be a GZip-compressed TAR file (.tgz, .tar.gz) or a YAML file (.yaml, .yml). Maximum size is 32MB.
name = 'name_example' # str | A name for this pipeline, optional (optional)
description = 'description_example' # str | A description for this pipeline, optional (optional)
annotations = 'annotations_example' # str | A string representation of a JSON dictionary of annotations describing this pipeline, optional. Example: {\"platform\": \"Kubeflow\", \"license\": \"Opensource\"} (optional)

try:
    api_response = api_instance.upload_pipeline(uploadfile, name=name, description=description, annotations=annotations)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PipelineServiceApi->upload_pipeline: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uploadfile** | **file**| The pipeline YAML file to upload. Can be a GZip-compressed TAR file (.tgz, .tar.gz) or a YAML file (.yaml, .yml). Maximum size is 32MB. | 
 **name** | **str**| A name for this pipeline, optional | [optional] 
 **description** | **str**| A description for this pipeline, optional | [optional] 
 **annotations** | **str**| A string representation of a JSON dictionary of annotations describing this pipeline, optional. Example: {\&quot;platform\&quot;: \&quot;Kubeflow\&quot;, \&quot;license\&quot;: \&quot;Opensource\&quot;} | [optional] 

### Return type

[**ApiPipelineExtended**](ApiPipelineExtended.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_pipeline_from_url**
> ApiPipeline upload_pipeline_from_url(url, name=name, access_token=access_token)



### Example
```python
from __future__ import print_function
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PipelineServiceApi()
url = 'url_example' # str | URL pointing to the pipeline YAML file.
name = 'name_example' # str | Optional, the name of the pipeline to be created overriding the name in the YAML file. (optional)
access_token = 'access_token_example' # str | Optional, the Bearer token to access the 'url'. (optional)

try:
    api_response = api_instance.upload_pipeline_from_url(url, name=name, access_token=access_token)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PipelineServiceApi->upload_pipeline_from_url: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **url** | **str**| URL pointing to the pipeline YAML file. | 
 **name** | **str**| Optional, the name of the pipeline to be created overriding the name in the YAML file. | [optional] 
 **access_token** | **str**| Optional, the Bearer token to access the &#39;url&#39;. | [optional] 

### Return type

[**ApiPipeline**](ApiPipeline.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

