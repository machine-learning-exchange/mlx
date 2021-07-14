## Deploy the MLX Stack on an Existing Kubernetes Cluster

To deploy the MLX single user mode on an existing Kubernetes Cluster, we can clone the MLX manifests and deploy it with Kustomize. This MLX deployment doesn't include model serving with KFServing. To experience the other MLX features such as KFServing, multi-user, and Istio mutual TLS, please install the extra plugins by follow one of the instructions on the [main README](/README.md/#2-deployment).

This MLX contains:
- Istio
- Kubeflow Pipeline single user
- Tekton Pipeline
- Datashim
- MLX

We will be using [kustomize 3.2.0](https://github.com/kubernetes-sigs/kustomize/releases/tag/v3.2.0) to align with Kubeflow's requirements because we will be also install kubeflow components as part of this MLX deployment.

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
