## Deploy the Minimum MLX Stack on an Existing Kubernetes Cluster

To deploy the minimum MLX on an existing Kubernetes Cluster, we can clone the MLX manifests and deploy it with Kustomize. The minimum MLX is only for running basic pipelines on MLX which doesn't support dataset deployment and model serving with KFServing. To experience the other MLX features, please follow one of the instructions on the [main README](/README.md/#2-deployment).

This minimum MLX contains:
- Istio
- Kubeflow Pipeline single user
- Tekton Pipeline
- MLX

We will be using [kustomize 3.2.0](https://github.com/kubernetes-sigs/kustomize/releases/tag/v3.2.0) to align with Kubeflow's requirements because we will be using kubeflow pipelines as the MLX pipeline engine. 
```
git clone https://github.com/machine-learning-exchange/manifests -b mlx-single-user
cd manifests
# run the below command two times if the CRDs take too long to provision.
while ! kustomize build example | kubectl apply -f -; do echo "Retrying to apply resources"; sleep 10; done
```
Then access the MLX page using http://<cluster_node_ip>:30380/mlx/
