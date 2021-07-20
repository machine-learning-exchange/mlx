# Deploy MLX on an existing Kubernetes cluster

## Prerequisites
* An existing Kubernetes cluster. Version 1.17+
* The minimum recommended capacity requirement for MLX is 8 vCPUs and 16GB RAM
* If you are using IBM Cloud, follow the appropriate instructions for standing up your Kubernetes cluster using [IBM Cloud Public](https://cloud.ibm.com/docs/containers?topic=containers-cs_cluster_tutorial#cs_cluster_tutorial)
* If you are using OpenShift on IBM Cloud, please follow the instructions for standing up your [IBM Cloud Red Hat OpenShift cluster](https://cloud.ibm.com/docs/containers?topic=containers-openshift_tutorial)
* [`kustomize v3.0+`](https://kubernetes-sigs.github.io/kustomize/installation/) is installed

## Deploy

To deploy the MLX single-user mode on an existing Kubernetes Cluster, clone the MLX manifests and deploy it with Kustomize. 

This MLX deployment includes:
- [Istio](https://istio.io/)
- [Kubeflow Pipelines](https://www.kubeflow.org/docs/components/pipelines/), single-user
- [Tekton Pipelines](https://github.com/tektoncd/pipeline#-tekton-pipelines)
- [Datashim](https://datashim-io.github.io/datashim/) to provide access to S3 and NFS Datasets within pods
- MLX API and UI

```shell
git clone https://github.com/machine-learning-exchange/manifests -b mlx-single-user
cd manifests
# run the below command two times if the CRDs take too long to provision.
while ! kustomize build example | kubectl apply -f -; do echo "Retrying to apply resources"; sleep 10; done
```

Then access the MLX web page on http://<cluster_node_ip>:30380/mlx/

This MLX deployment doesn't include or support:
- KFServing for model deployment
- Multi-user mode
- Istio mutual TLS

To get these features, please install the additional plugins by following the instructions for [MLX deployment an existing Kubeflow cluster](/docs/install-mlx-on-kubeflow.md#deploy-mlx-on-an-existing-kubeflow-cluster).

## Delete the MLX deployment

To delete this MLX deployment, run the following commands in the same manifests folder.

```
kustomize build example | kubectl delete -f -
```
