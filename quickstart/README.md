# Running MLX with Docker Compose

This _"quickstart"_ setup uses Docker Compose to bring up the MLX-API server and
the MLX Dashboard, along with the MySQL database and Minio S3 storage backend.
In this configuration, the preloaded asset catalog of Components, Datasets, Models
and Notebooks can be browsed, asset metadata and sample code can be downloaded
and new assets can be registered. Sample pipeline code can be generated for each
asset type, their execution on a Kubeflow Pipelines cluster is not enabled however.

## Limitations

The _Pipelines_ and _Inference Service_ capabilities are not available with this
Docker Compose setup. 

## Prerequisites

Install [Docker Compose](https://docs.docker.com/compose/install/). It might be
necessary to increase the Docker resources from the default of 2 GB memory to 4 GB.

Clone this repository:

    git clone https://github.com/machine-learning-exchange/mlx.git
    cd mlx

Navigate to the `quickstart` folder:

    cd quickstart


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


## Shut Down the Docker Containers

Press `control` + `c` on the Terminal to stop and then remove the containers:

    docker compose down -v

## Remove the Data Created by Minio and MySQL

    docker volume prune -f
