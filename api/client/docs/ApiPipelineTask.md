# ApiPipelineTask

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**artifact_type** | **str** | The type of artifact for this task, can be either one of: &#39;component&#39;, &#39;model&#39;, &#39;notebook&#39;, &#39;pipeline&#39; | 
**artifact_id** | **str** | The UUID of the artifact for this task | 
**arguments** | [**ApiPipelineTaskArguments**](ApiPipelineTaskArguments.md) |  | [optional] 
**dependencies** | **list[str]** | Task dependencies, referring to upstream tasks that have to be completed prior to running this task by their respective task names | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


