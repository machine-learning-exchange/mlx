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

<img src="docs/images/mlx.png" height="90%" width="90%">

Additionally it provides:

 - Automated sample pipeline code generation to execute registered models, datasets and notebooks
 - Pipelines engine powered by [Kubeflow Pipelines on Tekton](https://github.com/kubeflow/kfp-tekton), core of Watson AI Pipelines
 - Components registry for Kubeflow Pipelines
 - Datasets management by [Datashim](https://github.com/datashim-io/datashim)
 - Preregistered Datasets from [Data Asset Exchange (DAX)](https://developer.ibm.com/exchanges/data/) and Models from [Model Asset Exchange (MAX)](https://developer.ibm.com/exchanges/models/)
 - Serving engine by [KFServing](https://github.com/kubeflow/kfserving)
 - Model Metadata schemas

## 1. Deployment
<img src="docs/images/mlx-architecture-4.png" height="40%" width="40%">

For a simple up-and-running MLX with asset catalog only, we created a [Quickstart Guide](./quickstart) using [Docker Compose](https://docs.docker.com/compose/install/).

For a full deployment, we use [Kubeflow Kfctl](https://github.com/kubeflow/kfctl) tooling. 

* #### [MLX using Docker Compose (Asset Catalog Only)](./quickstart)

* #### [MLX Deployment on Kubernetes or OpenShift](./docs/mlx-setup.md)

* #### [MLX on an existing Kubeflow Cluster](./docs/install-mlx-on-kubeflow.md)


## 2. Access the MLX UI

1. By default the MLX UI is available at <public-ip-of-node>:30380/os

To find the public ip of a node of your cluster

```bash
kubectl get node -o wide
```
Look for the ExternalIP column.

2. If you are on a openshift cluster you can also make use of the IstioIngresGateway Route. You can find it in the OpenShift Console or in the CLI

```bash
oc get route -n istio-system
```

## 3. Import Data and AI Assets in MLX Catalog

[Import data and AI assets using MLX's catalog importer](/docs/import-assets.md)

## 4. Use MLX

Follow the [instructions here on how to use MLX once deployed](/docs/usage-steps.md)
	
## 5. Delete MLX

* Delete MLX deployment, the _KfDef_ instance

```shell
kubectl delete kfdef -n kubeflow --all
```

> Note that the users profile namespaces created by `profile-controller` will not be deleted. The `${KUBEFLOW_NAMESPACE}` created outside of the operator will not be deleted either.

* Delete Kubeflow Operator

```shell
kubectl delete -f deploy/operator.yaml -n ${OPERATOR_NAMESPACE}
kubectl delete clusterrolebinding kubeflow-operator
kubectl delete -f deploy/service_account.yaml -n ${OPERATOR_NAMESPACE}
kubectl delete -f deploy/crds/kfdef.apps.kubeflow.org_kfdefs_crd.yaml
kubectl delete ns ${OPERATOR_NAMESPACE}
```

## 6. Troubleshooting

* When deleting the Kubeflow deployment, some _mutatingwebhookconfigurations_ resources are cluster-wide resources and may not be removed as their owner is not the _KfDef_ instance. To remove them, run following:

	```shell
	kubectl delete mutatingwebhookconfigurations admission-webhook-mutating-webhook-configuration
	kubectl delete mutatingwebhookconfigurations inferenceservice.serving.kubeflow.org
	kubectl delete mutatingwebhookconfigurations istio-sidecar-injector
	kubectl delete mutatingwebhookconfigurations katib-mutating-webhook-config
	kubectl delete mutatingwebhookconfigurations mutating-webhook-configurations
	kubectl delete mutatingwebhookconfigurations cache-webhook-kubeflow
	```

* If you don't see any sample pipeline or receive `Failed to establish a new connection` messages. It's because IBM Cloud NFS storage might be taking too long to provision which makes the storage and backend microservices timed out. In this case, you have to run the below commands to restart the pods.
	```shell
	# Replace kubeflow with the KFP namespace
	NAMESPACE=kubeflow
	kubectl get pods -n ${NAMESPACE:-kubeflow}
	kubectl delete pod -n ${NAMESPACE:-kubeflow} $(kubectl get pods -n ${NAMESPACE:-kubeflow} -l app=ml-pipeline | grep ml-pipeline | awk '{print $1;exit}')
	kubectl delete pod -n ${NAMESPACE:-kubeflow} $(kubectl get pods -n ${NAMESPACE:-kubeflow} -l app=ml-pipeline-persistenceagent | grep ml-pipeline | awk '{print $1;exit}')
	kubectl delete pod -n ${NAMESPACE:-kubeflow} $(kubectl get pods -n ${NAMESPACE:-kubeflow} -l app=ml-pipeline-ui | grep ml-pipeline | awk '{print $1;exit}')
	kubectl delete pod -n ${NAMESPACE:-kubeflow} $(kubectl get pods -n ${NAMESPACE:-kubeflow} -l app=ml-pipeline-scheduledworkflow | grep ml-pipeline | awk '{print $1;exit}')
	```
	Then you can redeploy the bootstrapper to properly populate the default assets. Remember to insert the IBM Github Token if you want to retrieve any asset within IBM Github.
	```shell
	vim bootstrapper/bootstrap.yaml # Insert the IBM Github Token
	kubectl delete -f bootstrapper/bootstrap.yaml -n $NAMESPACE
	kubectl apply -f bootstrapper/bootstrap.yaml -n $NAMESPACE
	```

* Additional troubleshooting on IBM Cloud is available at [the wiki page](https://github.com/machine-learning-exchange/mlx/wiki/Troubleshooting).

## Join the Conversation
	
* Slack: [@lfaifoundation/ml-exchange](https://lfaifoundation.slack.com/archives/C0264LKNH63)
* Mailing lists:
  - [MLX-Announce](https://lists.lfaidata.foundation/g/mlx-announce) for top-level milestone messages and announcements
  - [MLX-TSC](https://lists.lfaidata.foundation/g/mlx-tsc) for top-level governance discussions and decissions
  - [MLX-Technical-Discuss](https://lists.lfaidata.foundation/g/mlx-technical-discuss) for technical discussions and questions
