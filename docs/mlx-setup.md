## Deploy MLX on an Existing Kubernetes Cluster

To deploy the minimum MLX on an existing Kubernetes Cluster, we can clone the MLX manifests and deploy it with Kustomize.

We will be using [kustomize 3.2.0](https://github.com/kubernetes-sigs/kustomize/releases/tag/v3.2.0) to align with Kubeflow's requirements because we will be using kubeflow pipelines as the MLX pipeline engine. 
```
git clone https://github.com/machine-learning-exchange/manifests -b mlx-single-user
cd manifests
# run the below command two times if the CRDs take too long to provision.
kustomize build example | kubectl apply -f -
```
Then access the MLX page using http://<cluster_node_ip>:30380/mlx/
