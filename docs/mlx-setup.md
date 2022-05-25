# Deploy MLX on an existing Kubernetes cluster

## Prerequisites
* An existing Kubernetes cluster:
   - **Min version: 1.17**
   - **Max version: 1.21** 
* The recommended minimum capacity requirement for MLX are: 
   - **CPUs**: 8 Cores
   - **Memory**: 16 GB RAM
   - **Disk**: 32+ GB
* If you are using IBM Cloud, follow the appropriate instructions for standing up your Kubernetes cluster using the [IBM Cloud Kubernetes Service](https://cloud.ibm.com/docs/containers?topic=containers-cs_cluster_tutorial#cs_cluster_tutorial)
* If you are using OpenShift on IBM Cloud, please follow the instructions for standing up your [IBM Cloud Red Hat OpenShift cluster](https://cloud.ibm.com/docs/openshift?topic=openshift-openshift_tutorial)
* [`kustomize v3.2.0`](https://github.com/kubernetes-sigs/kustomize/releases/tag/v3.2.0) is installed
   * Kustomize v3.2.0 quick install:
   ```
   OS=$(uname) 
   curl -L https://github.com/kubernetes-sigs/kustomize/releases/download/v3.2.0/kustomize_3.2.0_${OS}_amd64 --output kustomize
   chmod +x kustomize
   mv kustomize /usr/local/bin
   ```

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

## Troubleshooting

- If you see errors like these during the deployment, it may be because of a unsupported Kubernetes version.
  Check the [Prerequisites](#prerequisites) for the supported Kubernetes versions.
  
  ```
  # while ! kustomize build example | kubectl apply -f -; do echo "Retrying to apply resources"; sleep 10; done
  ...
  unable to recognize "STDIN": no matches for kind "CustomResourceDefinition" in version "apiextensions.k8s.io/v1beta1"
  unable to recognize "STDIN": no matches for kind "RoleBinding" in version "rbac.authorization.k8s.io/v1beta1"
  unable to recognize "STDIN": no matches for kind "ClusterRoleBinding" in version "rbac.authorization.k8s.io/v1beta1"
  unable to recognize "STDIN": no matches for kind "EnvoyFilter" in version "networking.istio.io/v1alpha3"
  ...
  ```
  To find your Kubernetes server version, run `kubectl version | grep Server`:
  ```
  Server Version: version.Info{Major:"1", Minor:"21", GitVersion:"v1.21.12", ...
  ```
