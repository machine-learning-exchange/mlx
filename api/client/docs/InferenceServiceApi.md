# swagger_client.InferenceServiceApi

All URIs are relative to *http://localhost/apis/v1alpha1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_service**](InferenceServiceApi.md#create_service) | **POST** /inferenceservices | 
[**get_inferenceservices**](InferenceServiceApi.md#get_inferenceservices) | **GET** /inferenceservices/{id} | 
[**list_inferenceservices**](InferenceServiceApi.md#list_inferenceservices) | **GET** /inferenceservices | 
[**upload_service**](InferenceServiceApi.md#upload_service) | **POST** /inferenceservices/upload | 


# **create_service**
> ApiInferenceservice create_service(body, namespace=namespace)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.InferenceServiceApi()
body = swagger_client.ApiInferenceservice() # ApiInferenceservice | 
namespace = 'namespace_example' # str |  (optional)

try:
    api_response = api_instance.create_service(body, namespace=namespace)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InferenceServiceApi->create_service: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ApiInferenceservice**](ApiInferenceservice.md)|  | 
 **namespace** | **str**|  | [optional] 

### Return type

[**ApiInferenceservice**](ApiInferenceservice.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_inferenceservices**
> ApiInferenceservice get_inferenceservices(id, namespace=namespace)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.InferenceServiceApi()
id = 'id_example' # str | 
namespace = 'namespace_example' # str |  (optional)

try:
    api_response = api_instance.get_inferenceservices(id, namespace=namespace)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InferenceServiceApi->get_inferenceservices: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **namespace** | **str**|  | [optional] 

### Return type

[**ApiInferenceservice**](ApiInferenceservice.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_inferenceservices**
> ApiListInferenceservicesResponse list_inferenceservices(page_token=page_token, page_size=page_size, sort_by=sort_by, filter=filter, namespace=namespace)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.InferenceServiceApi()
page_token = 'page_token_example' # str |  (optional)
page_size = 56 # int |  (optional)
sort_by = 'name' # str | Can be format of \"field_name\", \"field_name asc\" or \"field_name desc\" Ascending by default. (optional)
filter = '{"name": "test"}' # str | A string-serialized JSON dictionary with key-value pairs that correspond to the InferenceService's attribute names and their respective values to be filtered for. (optional)
namespace = 'kubeflow' # str |  (optional)

try:
    api_response = api_instance.list_inferenceservices(page_token=page_token, page_size=page_size, sort_by=sort_by, filter=filter, namespace=namespace)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InferenceServiceApi->list_inferenceservices: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page_token** | **str**|  | [optional] 
 **page_size** | **int**|  | [optional] 
 **sort_by** | **str**| Can be format of \&quot;field_name\&quot;, \&quot;field_name asc\&quot; or \&quot;field_name desc\&quot; Ascending by default. | [optional] 
 **filter** | **str**| A string-serialized JSON dictionary with key-value pairs that correspond to the InferenceService&#39;s attribute names and their respective values to be filtered for. | [optional] 
 **namespace** | **str**|  | [optional] 

### Return type

[**ApiListInferenceservicesResponse**](ApiListInferenceservicesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_service**
> ApiInferenceservice upload_service(uploadfile, name=name, namespace=namespace)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.InferenceServiceApi()
uploadfile = '/path/to/file.txt' # file | The inference service metadata to upload. Maximum size of 32MB is supported.
name = 'my inference service' # str |  (optional)
namespace = 'kubeflow' # str |  (optional)

try:
    api_response = api_instance.upload_service(uploadfile, name=name, namespace=namespace)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InferenceServiceApi->upload_service: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uploadfile** | **file**| The inference service metadata to upload. Maximum size of 32MB is supported. | 
 **name** | **str**|  | [optional] 
 **namespace** | **str**|  | [optional] 

### Return type

[**ApiInferenceservice**](ApiInferenceservice.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

