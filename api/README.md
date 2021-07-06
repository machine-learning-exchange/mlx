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

## Swagger Codegen 2.4

To generate our API we are using [`swagger-codegen`](https://github.com/swagger-api/swagger-codegen/tree/v2.4.8#prerequisites)
version [`2.4`](https://repo1.maven.org/maven2/io/swagger/swagger-codegen-cli/2.4.8/swagger-codegen-cli-2.4.8.jar)
as `swagger-codegen` version `3.0` no longer supports `python` server.

**Note**, Java 8 is **required** to run `swagger-codegen`. If not already installed, go to
[https://java.com/download](https://www.java.com/en/download/help/download_options.html).

It is **not required** to install `swagger-codegen` since the `generate_code.sh` script will
download it the first time it runs:

    # curl -L -O -s "https://repo1.maven.org/maven2/io/swagger/swagger-codegen-cli/2.4.8/swagger-codegen-cli-2.4.8.jar"
    # function swagger-codegen() { java -jar "swagger-codegen-cli-2.4.8.jar" "$@"; }
    # export -f swagger-codegen

It is **not recommended** to install [`swagger-codegen@2`](https://formulae.brew.sh/formula-linux/swagger-codegen@2)
via [Homebrew](https://docs.brew.sh/Installation) on macOS, since `brew install swagger-codegen@2`
does not allow selecting the _"old"_ version `2.4.8`. Instead, the `generate_code.sh` script
will automatically download the _"correct"_ version of the `swagger-codegen-cli.jar` file.

    # brew search swagger-codegen@
    # brew install swagger-codegen@2
    # brew link --force swagger-codegen@2

## Create a Python Virtual Environment for Development

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
