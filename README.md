[![Build Status](https://travis-ci.com/machine-learning-exchange/mlx.svg?branch=main)](https://travis-ci.com/machine-learning-exchange/mlx)
[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/4862/badge)](https://bestpractices.coreinfrastructure.org/projects/4862)
[![Slack](https://img.shields.io/badge/Slack-%40lfaifoundation%2Fml--exchange-blue.svg?logo=slack&logoColor=red)](https://lfaifoundation.slack.com/archives/C0264LKNH63)


# Machine Learning eXchange (MLX)

**Data and AI Assets Catalog and Execution Engine** 

Allows upload, registration, execution, and deployment of:
 - AI pipelines and pipeline components
 - Models
 - Datasets
 - Notebooks

Additionally it provides:

 - Automated sample pipeline code generation to execute registered models, datasets and notebooks
 - Pipelines engine powered by [Kubeflow Pipelines on Tekton](https://github.com/kubeflow/kfp-tekton), core of Watson AI Pipelines
 - Components registry for Kubeflow Pipelines
 - Datasets management by [Datashim](https://github.com/datashim-io/datashim)
 - Preregistered Datasets from [Data Asset Exchange (DAX)](https://developer.ibm.com/exchanges/data/) and Models from [Model Asset Exchange (MAX)](https://developer.ibm.com/exchanges/models/)
 - Serving engine by [KFServing](https://github.com/kubeflow/kfserving)
 - Model Metadata schemas

For more details about the project check out this [announcement blog post](https://lfaidata.foundation/blog/2021/09/28/machine-learning-exchange-mlx/). 


<img src="docs/images/mlx.png" height="90%" width="90%">


## 1. Deployment
<img src="docs/images/mlx-architecture-4.png" height="40%" width="40%">

For a simple up-and-running MLX with asset catalog only, we created a [Quickstart Guide](./quickstart)
using [Docker Compose](https://docs.docker.com/compose/install/).

For a slightly more resource-hungry local deployment that allows pipeline execution, we created the
[MLX with Kubernetes in Docker (KIND)](./docs/install-mlx-on-kind.md) deployment option.

For a full deployment, we use [Kubeflow Kfctl](https://github.com/kubeflow/kfctl) tooling. 

* #### [MLX using Docker Compose (Asset Catalog Only)](./quickstart)

* #### [MLX on Kubernetes in Docker (Fully Featured)](./docs/install-mlx-on-kind.md)

* #### [MLX Deployment on Kubernetes or OpenShift](./docs/mlx-setup.md)

* #### [MLX on an existing Kubeflow Cluster](./docs/install-mlx-on-kubeflow.md)


## 2. Access the MLX UI

By default, the MLX UI is available at http://<cluster_node_ip>:30380/mlx/

If you deployed on a **Kubernetes** cluster, run the following and look for the External-IP column to find the public IP of a node.

```bash
kubectl get node -o wide
```

If you deployed using **OpenShift**, you can use IstioIngresGateway Route. You can find it in the OpenShift Console or using the CLI.

```bash
oc get route -n istio-system
```

## 3. Import Data and AI Assets in MLX Catalog

For information on how to import data and AI assets using MLX's catalog importer, use this [guide](/docs/import-assets.md).

## 4. Use MLX

For information on how to use MLX and create assets check out this [guide](/docs/usage-steps.md).

## 5. How to Contribute

For information about adding new features, bug fixing, communication
or UI and API setup, refer to this [document](CONTRIBUTING.md).


## 6. Troubleshooting

[MLX Troubleshooting Instructions](/docs/troubleshooting.md)
	
## Join the Conversation
	
* Slack: [@lfaifoundation/ml-exchange](https://lfaifoundation.slack.com/archives/C0264LKNH63)
* Mailing lists:
  - [MLX-Announce](https://lists.lfaidata.foundation/g/mlx-announce) for top-level milestone messages and announcements
  - [MLX-TSC](https://lists.lfaidata.foundation/g/mlx-tsc) for top-level governance discussions and decissions
  - [MLX-Technical-Discuss](https://lists.lfaidata.foundation/g/mlx-technical-discuss) for technical discussions and questions
