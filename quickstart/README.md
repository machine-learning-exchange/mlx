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

* Install [Docker Compose](https://docs.docker.com/compose/install/).
* It may be necessary to increase the [Docker resources](https://docs.docker.com/docker-for-mac/#resources) from the
default of 2 GB memory to 4 GB.
* Approximately 10 GB of free storage

Clone this repository and navigate to the `quickstart` folder:

    git clone https://github.com/machine-learning-exchange/mlx.git
    cd mlx/quickstart

## Keep up to date

If some time has passed since the `mlx` repository was cloned, 
make sure to pull the latest sources for the _Quickstart_:

    git pull

## Pull the Docker Images

Our Docker images for the [mlx-api](https://hub.docker.com/r/mlexchange/mlx-api/tags?name=nightly)
and [mlx-ui](https://hub.docker.com/r/mlexchange/mlx-ui/tags?name=nightly) 
get rebuilt nightly. To get the latest version, run:

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

## Troubleshooting

If you are working on a local clone of your fork, rather than a clone of the source
repository, make sure to keep your code up to date:

    git remote add upstream https://github.com/machine-learning-exchange/mlx.git
    git fetch upstream
    git checkout main
    git rebase upstream/main
    git push origin main --force

Since we are actively developing MLX, there may have been changes to the data schema
which could conflict with the data created by running the Quickstart in days prior.
The symptoms of this could be empty dashboards with endlessly spinning wheels.
To remove all previously created Docker Compose data run the following commands:

    docker compose down -v --remove-orphans
    docker compose rm -v -f
    docker volume prune -f
    
### Windows Subsystem for Linux (WSL) Issues

#### Quickstart - init_catalog.sh
After you run:

    docker compose up
If you are experiencing the below error with the init_catalog.sh file not being found by docker:

    catalog_1     | /bin/sh: /init_catalog.sh: not found
    catalog_1 exited with code 127
Make sure you originally cloned/forked the source repo from WSL, not Windows. Error happens because you have files with Windows line endings which bash cannot run (https://askubuntu.com/questions/966488/how-do-i-fix-r-command-not-found-errors-running-bash-scripts-in-wsl#comment1553686_966488).
The error prevents loading of assets and objects into the MLX UI.

