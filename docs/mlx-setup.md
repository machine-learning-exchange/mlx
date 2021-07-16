# Deploy MLX on an existing Kubernetes cluster

## Prerequisites
* An existing Kubernetes cluster. Version 1.17+
* The minimum recommended capacity requirement for MLX is 8 vCPUs and 16GB RAM
* If you are using IBM Cloud, follow the appropriate instructions for standing up your Kubernetes cluster using [IBM Cloud Public](https://cloud.ibm.com/docs/containers?topic=containers-cs_cluster_tutorial#cs_cluster_tutorial)
* If you are using OpenShift on IBM Cloud, please follow the instructions for standing up your [IBM Cloud Red Hat OpenShift cluster](https://cloud.ibm.com/docs/containers?topic=containers-openshift_tutorial)
* [`kustomize v3.0+`](https://kubernetes-sigs.github.io/kustomize/installation/) is installed

To deploy the MLX single user mode on an existing Kubernetes Cluster, clone the MLX manifests and deploy it with Kustomize. 

This MLX deployment includes:
- Istio
- Kubeflow Pipeline single user
- Tekton Pipeline
- Datashim
- MLX

We are using [kustomize 3.2.0](https://github.com/kubernetes-sigs/kustomize/releases/tag/v3.2.0) to align with Kubeflow's requirements because we will install kubeflow components as part of this MLX deployment.

```shell
git clone https://github.com/machine-learning-exchange/manifests -b mlx-single-user
cd manifests
# run the below command two times if the CRDs take too long to provision.
while ! kustomize build example | kubectl apply -f -; do echo "Retrying to apply resources"; sleep 10; done
```
Then access the MLX page using http://<cluster_node_ip>:30380/mlx/


## Delete the MLX deployment

To delete the above MLX deployment, simply run the following commands in the same repo.

```
kustomize build example | kubectl delete -f -
```
