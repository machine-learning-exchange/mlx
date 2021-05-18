# Running MLX with Docker Compose

This _"quickstart"_ setup uses  [Docker Compose](https://docs.docker.com/compose/)
to bring up the MLX API server and the MLX Dashboard, together with the MySQL
database and Minio S3 storage backend.
In this configuration, the preloaded asset catalog of Components, Datasets, Models,
Notebooks and Pipelines can be browsed, asset metadata and sample code can be
downloaded and new assets can be registered. Sample pipeline code can be generated
for each asset type, however their execution on a Kubeflow Pipelines (KFP) cluster
is not enabled.
In a Kubernetes cluster deployment of MLX, _Pipelines_ are registered using
the KFP API and metadata storage is managed by KFP. In this Docker Compose setup
the _Pipelines_ are stored in Minio and MySQL by the MLX API server.

## Limitations

The _Kubeflow Pipelines_ dashboard and _Inference Service_ capabilities are not
available with this Docker Compose setup.

## Prerequisites

Install [Docker Compose](https://docs.docker.com/compose/install/). It may be
necessary to increase the
[Docker resources](https://docs.docker.com/docker-for-mac/#resources) from the
default of 2 GB memory to 4 GB.

Clone this repository and navigate to the `quickstart` folder:

    git clone https://github.com/machine-learning-exchange/mlx.git
    cd mlx/quickstart

## Pull the Docker Images

    docker compose pull

## Bring up the Docker Containers

    docker compose up

Wait for the containers to start up. When the MLX API and UI are ready, this
message should show up in the terminal log:

```Markdown
dashboard_1   | 
dashboard_1   | ================================================
dashboard_1   |  Open the MLX Dashboard at http://localhost:80/ 
dashboard_1   | ================================================
dashboard_1   | 
```

Now open a web browser and type `localhost` in the address bar to open the MLX
dashboard.

The MLX API spec can be explored at `localhost:8080/apis/v1alpha1/ui/`

**Note:** If the Docker compose stack is running on a remote host, and the
MLX Web UI is running on `localhost`, export the environment
variable `DOCKER_HOST_IP`, so that the MLX UI web app on `localhost` can connect
to the MLX API on the Docker host.

    export DOCKER_HOST_IP=127.0.0.1
    docker compose up

## Shut Down the Docker Containers

Press `control` + `c` on the Terminal to stop and then remove the containers:

    docker compose down -v

## Remove the Data Created by Minio and MySQL

    docker volume prune -f
