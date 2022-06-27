# swagger_client.ApplicationSettingsApi

All URIs are relative to *http://localhost/apis/v1alpha1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_application_settings**](ApplicationSettingsApi.md#get_application_settings) | **GET** /settings | 
[**modify_application_settings**](ApplicationSettingsApi.md#modify_application_settings) | **PUT** /settings | 
[**set_application_settings**](ApplicationSettingsApi.md#set_application_settings) | **POST** /settings | 


# **get_application_settings**
> ApiSettings get_application_settings()



Returns the application settings.

### Example
```python
from __future__ import print_function
import time
import swagger_client  # noqa: F401
from swagger_client.rest import ApiException  # noqa: F401
from pprint import pprint  # noqa: F401

# create an instance of the API class
api_instance = swagger_client.ApplicationSettingsApi()

try:
    api_response = api_instance.get_application_settings()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ApplicationSettingsApi->get_application_settings: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**ApiSettings**](ApiSettings.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **modify_application_settings**
> ApiSettings modify_application_settings(dictionary)



Modify one or more of the application settings.

### Example
```python
from __future__ import print_function
import time
import swagger_client  # noqa: F401
from swagger_client.rest import ApiException  # noqa: F401
from pprint import pprint  # noqa: F401

# create an instance of the API class
api_instance = swagger_client.ApplicationSettingsApi()
dictionary = swagger_client.Dictionary() # Dictionary | A dictionary where the name of the keys corresponds to the name of the settings.

try:
    api_response = api_instance.modify_application_settings(dictionary)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ApplicationSettingsApi->modify_application_settings: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dictionary** | [**Dictionary**](Dictionary.md)| A dictionary where the name of the keys corresponds to the name of the settings. | 

### Return type

[**ApiSettings**](ApiSettings.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_application_settings**
> ApiSettings set_application_settings(settings)



Set and store the application settings.

### Example
```python
from __future__ import print_function
import time
import swagger_client  # noqa: F401
from swagger_client.rest import ApiException  # noqa: F401
from pprint import pprint  # noqa: F401

# create an instance of the API class
api_instance = swagger_client.ApplicationSettingsApi()
settings = swagger_client.ApiSettings() # ApiSettings | 

try:
    api_response = api_instance.set_application_settings(settings)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ApplicationSettingsApi->set_application_settings: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **settings** | [**ApiSettings**](ApiSettings.md)|  | 

### Return type

[**ApiSettings**](ApiSettings.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

