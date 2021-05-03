# swagger_client.CredentialServiceApi

All URIs are relative to *http://localhost/apis/v1alpha1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_credential**](CredentialServiceApi.md#create_credential) | **POST** /credentials | 
[**delete_credential**](CredentialServiceApi.md#delete_credential) | **DELETE** /credentials/{id} | 
[**get_credential**](CredentialServiceApi.md#get_credential) | **GET** /credentials/{id} | 
[**list_credentials**](CredentialServiceApi.md#list_credentials) | **GET** /credentials | 


# **create_credential**
> ApiCredential create_credential(body)



Creates a credential associated with a pipeline.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.CredentialServiceApi()
body = swagger_client.ApiCredential() # ApiCredential | 

try:
    api_response = api_instance.create_credential(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CredentialServiceApi->create_credential: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ApiCredential**](ApiCredential.md)|  | 

### Return type

[**ApiCredential**](ApiCredential.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_credential**
> delete_credential(id)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.CredentialServiceApi()
id = 'id_example' # str | 

try:
    api_instance.delete_credential(id)
except ApiException as e:
    print("Exception when calling CredentialServiceApi->delete_credential: %s\n" % e)
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

# **get_credential**
> ApiCredential get_credential(id)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.CredentialServiceApi()
id = 'id_example' # str | 

try:
    api_response = api_instance.get_credential(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CredentialServiceApi->get_credential: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**ApiCredential**](ApiCredential.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_credentials**
> ApiListCredentialsResponse list_credentials(page_token=page_token, page_size=page_size, sort_by=sort_by, filter=filter)



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.CredentialServiceApi()
page_token = 'page_token_example' # str |  (optional)
page_size = 56 # int |  (optional)
sort_by = 'name' # str | Can be format of \"field_name\", \"field_name asc\" or \"field_name desc\" Ascending by default. (optional)
filter = '{"name": "test"}' # str | A string-serialized JSON dictionary with key-value pairs that correspond to the Credential's attribute names and their respective values to be filtered for. (optional)

try:
    api_response = api_instance.list_credentials(page_token=page_token, page_size=page_size, sort_by=sort_by, filter=filter)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CredentialServiceApi->list_credentials: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page_token** | **str**|  | [optional] 
 **page_size** | **int**|  | [optional] 
 **sort_by** | **str**| Can be format of \&quot;field_name\&quot;, \&quot;field_name asc\&quot; or \&quot;field_name desc\&quot; Ascending by default. | [optional] 
 **filter** | **str**| A string-serialized JSON dictionary with key-value pairs that correspond to the Credential&#39;s attribute names and their respective values to be filtered for. | [optional] 

### Return type

[**ApiListCredentialsResponse**](ApiListCredentialsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

