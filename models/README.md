# Models

MLX supports the use of pre-trained models.

## Create Model Metadata
Below are the 2 minimal templates to create a trainable or servable model metadata. You can visit [samples](samples) to view some examples or [template](template/model.yaml) to view the model metadata spec details.
#### trainable model metadata template
```
name: <model_name>
model_identifier: <model_id>
description: <model_description>
author:
  name: "IBM CODAIT"
  email: "no-reply@ibm.com"
framework:
  name: "tensorflow"
  version: "1.5"
  runtimes:
      name: python
      version: "3.5"

license: "Apache 2.0"
domain: "Domain Area"
website: <model_website> # Can be GitHub link

train:
  trainable: true
  credentials_required: true
  tested_platforms:
    - WatsonML
  model_source:
    initial_model:
      data_store: cloud_training_datastore
      bucket: <data_bucket_name>
      path: model.zip
  model_training_results:
    trained_model:
      data_store: cloud_training_datastore
      bucket: <data_result_name>
  data_source:
    training_data:
      data_store: cloud_training_datastore
      bucket: <data_bucket_name>
      path: aligned
  mount_type: mount_cos
  execution:
    command: ./train-max-model.sh
    compute_configuration:
      name: k80
      nodes: 1
process:
    - name: training_process
      params:
       staging_dir: training_output/
       trained_model_path: trained_model/tensorflow/checkpoint/
data_stores:
  - name: cloud_training_datastore
    type: s3
    connection:
      endpoint: https://s3.us.cloud-object-storage.appdomain.cloud
```


#### servable model metadata template
```shell
name: <model_name>
model_identifier: <model_id>
description: <model_description>
framework:
  name: "tensorflow"
  version: "1.8.0"

license: "Apache 2.0"
domain: "Domain Area"
website: <model_website> # Can be GitHub link

serve:
  servable: true
  tested_platforms:
    - kubernetes
    - knative
  serving_container_image:
    container_image_url: <model_docker_image>
```

## Register Model
1. Click on the "Models" link in left hand navigation panel
2. Click on "UPLOAD A COMPONENT"
3. Select a file to upload (Must be tar.gz or tgz format)
    * This will be the compressed .yaml specification
4. Enter a name for the model; Otherwise a default will be given

## Use Models in Pipelines
Models can easily be executed based on the metadata specified in the yaml file for a particular function

1. Under the models tab, select a model
2. Switch to the "CREATE RUN" section
3. Give the name a run and click submit to serve the model
