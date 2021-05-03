# Jupyter Notebook Execution

## Intended Use
Run a jupyter notebook as a component in a pipeline, and save the output notebook to object storage. Notebook execution is made up of 3 main steps:
1. Download the jupyter notebook from github
2. Process the notebook via papermill
3. Write the output notebook to object storage
  
## Run-Time Parameters:
Name | Description
:--- | :----------
notebook_url | Required. Github url for a jupyter notebook
notebook_params | Optional. JSON string representation of parameters consumed by papermill
api_token | Optional. API token for private/enterprise repositories
endpoint_url | Required. Endpoint url for the storage instance
bucket_name | Required. Bucket name to write output to
object_name | Required. Object name to write output notebook to
access_key | Required. Access key id
secret_access_key | Required. Secret access key

## Output:
Name | Description
:--- | :----------

## Execution

Run as standalone python code, or within a docker container

#### Python 3
```bash
pip3 install -r requirements.txt

python3 src/execute_notebook.py \
    --notebook_url https://github.ibm.com/Evan-Hataishi/test-notebooks/blob/master/temp.ipynb \
    --api_token 9488520d68292ad76a1ac3f02bd75976a12650f0 \
    --endpoint_url http://s3.us-south.cloud-object-storage.appdomain.cloud \
    --bucket_name evan-1 \
    --object_name my_file.ipynb \
    --access_key 1152b0126f7e44ed8e000169055030c5 \
    --secret_access_key 20d44f6326349e46da17a2343cb4a98ad6177896784606ec \
    --notebook_params '{"message": "my message"}'
```

#### Docker
```bash
docker run notebook-execution:latest \
    --notebook_url https://github.ibm.com/Evan-Hataishi/test-notebooks/blob/master/temp.ipynb \
    --api_token 9488520d68292ad76a1ac3f02bd75976a12650f0 \
    --endpoint_url http://s3.us-south.cloud-object-storage.appdomain.cloud \
    --bucket_name evan-1 \
    --object_name my_file.ipynb \
    --access_key 1152b0126f7e44ed8e000169055030c5 \
    --secret_access_key 20d44f6326349e46da17a2343cb4a98ad6177896784606ec \
    --notebook_params '{"message": "my message"}'
```

## Docker
```bash
// Build the container
docker build -t notebook-execution:latest .

// Tag the image with dockerhub
docker tag image_id aipipeline/notebook-execution:latest

// Push to dockerhub
docker push aipipeline/notebook-execution:latest

// Run the container
docker run notebook-execution \
    --notebook_url ... \
    ... \
    ...
```