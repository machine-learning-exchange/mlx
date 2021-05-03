# Copyright 2021 IBM Corporation 
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License. 
import argparse
import papermill as pm
import json
from sys import stderr

from storage_client import StorageClient
from github_client import GithubClient


def json_string_to_dict(params):
    if not params:
        return {}

    params = params.replace("\'", "\"")

    try:
        parsed_params = json.loads(params)
    except Exception as err:
        raise Exception("Unable to parse parameters:\n %s" % err)

    return parsed_params


# Save output locally to a file name given by the object_name
def run_papermill(notebook_name, object_name, params):
    output_notebook_name = object_name.split('/')[-1]
    try:
        pm.execute_notebook(
            input_path=notebook_name,
            output_path=output_notebook_name,
            kernel_name='python3',
            progress_bar=False,
            parameters=params,
            log_output=True
        )
    except Exception as err:
        raise Exception("Error while executing notebook:\n %s" % err)

    return output_notebook_name


def main(notebook_url, notebook_params, api_token, endpoint_url, bucket_name, object_name, access_key, secret_access_key):
    print("- Initializing github client")
    github_client = GithubClient(api_token)

    print("- Initializing object storage client")
    storage_client = StorageClient(endpoint_url, access_key, secret_access_key)

    try:
        print("- Downloading notebook: %s" % notebook_url)
        notebook_name = github_client.download_file(notebook_url)
        print("- Download successful")

        print("- Parsing notebook parameters")
        param_dict = json_string_to_dict(notebook_params)
        print("- Parameter parsing successful")

        print("- Executing notebook: %s" % notebook_name)
        print("- Notebook Parameters: %s" % str(param_dict))
        processed_notebook = run_papermill(notebook_name, object_name, param_dict)
        print("- Notebook execution successful. Output saved locally to %s" % processed_notebook)

        print("- Uploading processed notebook to %s in %s" % (object_name, bucket_name))
        storage_client.upload_file(processed_notebook, bucket_name, object_name)
        print("- Notebook upload successful")
    except Exception as err:
        print(err, file=stderr)
        exit(1)

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--notebook_url', type=str, help='Github url for the jupyter notebook to be run')
    parser.add_argument('--notebook_params', type=str, help='JSON string representation of parameters consumed by papermill')
    parser.add_argument('--api_token', type=str, help='API token for private/enterprise repositories')
    parser.add_argument('--endpoint_url', type=str, help='Endpoint url for the storage instance')
    parser.add_argument('--bucket_name', type=str, help='Bucket name to write output to')
    parser.add_argument('--object_name', type=str, help='Object name to write output notebook to')
    parser.add_argument('--access_key', type=str, help='Storage access key id')
    parser.add_argument('--secret_access_key', type=str, help='Storage secret access key')
    args = parser.parse_args()

    main(args.notebook_url, args.notebook_params, args.api_token, args.endpoint_url, args.bucket_name, args.object_name, args.access_key, args.secret_access_key)
