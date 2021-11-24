# Machine Learning Exchange - Web UI

## Setup

This repo contains the code for the front end UI of the Machine Learning Exchange project.

To run this app, you'll need a current version of Node.js installed.

1. First, clone this repo:
```Bash
git clone https://github.com/machine-learning-exchange/mlx.git
```

2. Next, install the dependencies by running this command from within the newly created directory:
```Bash
npm install
```

3. Start the app with the following command:
```Bash
npm start
```

4. The app should now be accessible in your web browser at:
```
http://localhost:3000
```

## Configure usage of MLX API and KFP API

If an MLX or KFP API is already deployed you can connect it to the UI in one of the following ways

* Set the respective environment variable to the endpoint of the API before running npm start

```Bash
REACT_APP_API=<MLX API Endpoint>
REACT_APP_KFP=<KFP API Endpoint
npm start
```

* Configure the API endpoints in the settings page of the UI at
```
http://localhost:3000/settings
```

## Deploy MLX UI to Kubernetes

First deploy the MLX UI.
```Bash
kubectl apply -f ./dashboard/origin-mlx/mlx-ui.yml
```

Find the UI Host and Port. It may take some time before the MLX UI becomes available.
```Bash
export UI_HOST=$(kubectl get nodes -o jsonpath='{.items[].status.addresses[?(@.type=="ExternalIP")].address}')
export UI_PORT=$(kubectl get service mlx-ui -n kubeflow -o jsonpath='{.spec.ports[0].nodePort}')
```
Open the webpage in a browser:

```Bash
open "http://${UI_HOST}:${UI_PORT}"
```

# Development Setup

## Build a Docker Image for MLX UI

```Bash
cd dashboard/origin-mlx
docker build -t <your docker user-id>/<repo name>:<tag name> -f Dockerfile .
docker push <your docker user-id>/<repo name>:<tag name>
```

## (Re-)Deploy to Kubernetes Cluster

Change the Docker image tag in the deployment spec server/mlx-ui.yml from image: ibmandrewbutler/open-ui:add-homepage to image: <your_docker_user_id>/<repo name>:<tag name> and then run:

```Bash
kubectl delete -f ./dashboard/origin-mlx/mlx-ui.yml
kubectl apply -f ./dashboard/origin-mlx/mlx-ui.yml
```

## UI Development with Docker Compose

You can test most code changes without a Kubernetes cluster. A K8s cluster is only
required to `run` the generated sample pipeline code. Running the Quickstart with
Docker Compose is sufficient to test any `katalog` related API endpoints.

A development setup that works very well requires to 2 shell terminals:

### Terminal 1 - Quickstart without `mlx-ui` service

Bring up the Quickstart without the `mlx-ui` service, since we will run the MLX UI
from our local source code, instead of using the pre-built Docker image `mlexchange/mlx-ui:nightly-origin-main`.

```Bash
# cd <mlx_root_directory>
cd quickstart

docker compose --project-name  no_ui   up   minio miniosetup mysql mlx-api catalog
```

Remember to bring down the Docker Compose stack after testing your UI code changes:

```Bash
# control + C 

docker compose --project-name  no_ui  down  minio miniosetup mysql mlx-api catalog
```

Optional, to delete all data in Minio and MySQL, run the following commands:

```Bash
docker compose down -v --remove-orphans
docker compose rm -v -f
docker volume prune -f
```

### Terminal 2 - Start the UI server

Navigate to the UI source folder:

```Bash
# cd <mlx_root_directory>
cd dashboard/origin-mlx
```

Install the package dependencies:

```Bash
rm -f package-lock.json  # this may be necessary to prevent npm install errors
npm install
```

Set the `REACT_APP_API` environment variable so the MLX UI can connect to the MLX API
backend from the Docker Compose stack:

```Bash
export REACT_APP_API="localhost:8080"
export REACT_APP_RUN="false"
export REACT_APP_UPLOAD="true"
export REACT_APP_DISABLE_LOGIN="true"
export REACT_APP_TTL="0"                # Disable the cache
export REACT_APP_CACHE_INTERVAL="0"     # Ignore checking cache
```

Start the MLX Web UI server:

```Bash
npm start
```

The MLX web UI should open up in your web browser at:

```
http://localhost:3000/
```

After testing the UI stop the `npm` server with `control` + `C`


# Special Configurations

There are a few environment variables that can be defined that dictate how MLX is deployed

* `REACT_APP_API` - The endpoint for the MLX API
* `REACT_APP_KFP` - The endpoint for the KFP API
* `REACT_APP_NBVIEWER_API` - The endpoint for the Notebook Viewer API
* `REACT_APP_KIALI` - The endpoint for Kiali monitoring
* `REACT_APP_GRAFANA` - The endpoint for the Grafana service
* `HTTPS` - true/false, defines whether HTTPS or HTTP should be used
* `REACT_APP_BASE_PATH` - A basepath can be configured that appends to the end of the address (ex.
  http://<ip_address>:<port>/<basepath>)
* `REACT_APP_BRAND` - The brand name to use on the website
* `REACT_APP_DISABLE_LOGIN` - A switch to turn off login mechanism
* `REACT_APP_TTL` - The amount of seconds a cached entry remains valid for (24 hours by default)
* `REACT_APP_CACHE_INTERVAL` - The minimum amount of time in seconds between two checks on the validity of the cache's contents (24 hours by default)

# Caching Details

The cache stores each request and response pair made from the UI to the API in local storage. If a request is made 
which matches a previous request and the difference of the time between the two requests is less than `REACT_APP_TTL` then the previously recorded response is returned. Every `REACT_APP_CACHE_INTERVAL` seconds a new check on the validity of the cache can be run. Whenever the UI is refreshed a check will be made if enough time has passed since the last cache validity check, if so then a cache validity check is started. Any item in the cache which has lasted longer than `REACT_APP_TTL` seconds is removed from the cache.

To invalidate or hard reset the cache, navigate to the settings page (clicking the three dots at the bottom of the sidebar) and click on the `Reset Cache` button.

# Project Overview:

![MLX Overview](src/images/image1.png)
