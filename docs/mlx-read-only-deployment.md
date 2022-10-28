## Deploy the MLX Read-Only mode on an Existing Kubernetes Cluster

To deploy MLX in read-only mode on an existing Kubernetes cluster without Kubeflow, clone the MLX repo and apply the manifest using Kustomize:

```shell
git clone https://github.com/machine-learning-exchange/mlx
cd mlx
kubectl apply -k manifests/read-only-k8s
```

To delete the read-only deployment, run
```
kubectl delete -k manifests/read-only-k8s
```
