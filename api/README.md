# Machine Learning Exchange API - Python Client and Python-Flask Server

An extension to the Kubeflow Pipeline API for Components and Models


# Quickstart    

## Deploy to Kubernetes

    kubectl apply -f ./server/mlx-api.yml

## Find API Server Host and Port

    export API_HOST=$(kubectl get nodes -o jsonpath='{.items[].status.addresses[?(@.type=="ExternalIP")].address}')
    export API_PORT=$(kubectl get service mlx-api -n kubeflow -o jsonpath='{.spec.ports[0].nodePort}')

## Open the Swagger UI in a Web Browser

    open "http://${API_HOST}:${API_PORT}/apis/v1alpha1/ui/"
    
---

# Development Setup

## Swagger CLI

    npm install -g swagger-cli

## Python Virtual Environment for Development

    python3 -m venv .venv
    source .venv/bin/activate

    # force pip to use legacy dependency version conflict resolver
    # "kfserving 0.4.1 requires kubernetes==10.0.1, but you'll have kubernetes 11.0.0 which is incompatible."
    export PYTHON_PIP_VERSION=20.2.4
    pip install pip=="$PYTHON_PIP_VERSION" --force-reinstall

    pip install -r ./requirements.txt

## (Re-)Generate Swagger Client and Server Code

    ./generate_code.sh

## Build the Docker Image

    cd server
    docker build -t <your_docker_user_id>/mlx-api-server:0.1 .
    docker login
    docker push <your_docker_user_id>/mlx-api-server:0.1

## (Re-)Deploy to Kubernetes Cluster

Change the Docker image tag in the deployment spec `server/mlx-api.yml` 
from `image: docker.io/aipipeline/mlx-api:nightly-master` 
to `image: docker.io/<your_docker_user_id>/mlx-api-server:0.1`
and then run:

    ./api/deploy.sh

or:

    kubectl delete -f ./server/mlx-api.yml
    kubectl apply -f ./server/mlx-api.yml

## Latest Swagger Codegen

  We are using Swagger `2.4.8` for our API due to some inconsistency with the latest Swagger on Mac.
  Below are the instructions for pulling the latest Swagger using brew, but we will not be using it
  for our general development.

  **Note:** `swagger-codegen` `3.0.x` does not support Python (server) anymore, 
  so we need to downgrade to version 2.x:

    brew search swagger-codegen@
    brew install swagger-codegen@2
    brew link --force swagger-codegen@2
