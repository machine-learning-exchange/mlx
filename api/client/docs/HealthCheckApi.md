# swagger_client.HealthCheckApi

All URIs are relative to *http://localhost/apis/v1alpha1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**health_check**](HealthCheckApi.md#health_check) | **GET** /health_check | Checks if the server is running


# **health_check**
> health_check(check_database=check_database, check_object_store=check_object_store)

Checks if the server is running

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.HealthCheckApi()
check_database = true # bool | Test connection to MySQL database (optional)
check_object_store = true # bool | Test connection to Minio object store (optional)

try:
    # Checks if the server is running
    api_instance.health_check(check_database=check_database, check_object_store=check_object_store)
except ApiException as e:
    print("Exception when calling HealthCheckApi->health_check: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **check_database** | **bool**| Test connection to MySQL database | [optional] 
 **check_object_store** | **bool**| Test connection to Minio object store | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

