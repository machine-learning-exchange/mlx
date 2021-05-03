# ApiModel

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**name** | **str** |  | 
**description** | **str** |  | 
**featured** | **bool** |  | [optional] 
**publish_approved** | **bool** |  | [optional] 
**related_assets** | **list[str]** |  | [optional] 
**domain** | **str** |  | [optional] 
**labels** | **dict(str, str)** |  | [optional] 
**framework** | [**ApiModelFramework**](ApiModelFramework.md) |  | 
**trainable** | **bool** |  | [optional] 
**trainable_tested_platforms** | **list[str]** |  | [optional] 
**trainable_credentials_required** | **bool** |  | [optional] 
**trainable_parameters** | [**list[ApiParameter]**](ApiParameter.md) |  | [optional] 
**servable** | **bool** |  | [optional] 
**servable_tested_platforms** | **list[str]** |  | [optional] 
**servable_credentials_required** | **bool** |  | [optional] 
**servable_parameters** | [**list[ApiParameter]**](ApiParameter.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


