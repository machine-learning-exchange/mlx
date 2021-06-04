# ApiPipelineExtended

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**parameters** | [**list[ApiParameter]**](ApiParameter.md) |  | [optional] 
**status** | **str** | In case any error happens retrieving a pipeline field, only pipeline ID and the error message is returned. Client has the flexibility of choosing how to handle error. This is especially useful during listing call. | [optional] 
**default_version_id** | **str** | The default version of the pipeline. As of now, the latest version is used as default. (In the future, if desired by customers, we can allow them to set default version.) | [optional] 
**namespace** | **str** |  | [optional] 
**annotations** | **dict(str, str)** |  | [optional] 
**featured** | **bool** |  | [optional] 
**publish_approved** | **bool** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


