
## Deploy the MLX ReadOnly mode on an Existing Kubernetes Cluster

To deploy the minimum MLX on an existing Kubernetes Cluster, we can clone the MLX manifests and deploy it with Kustomize. The minimum MLX is only for Read only. To deploy the MLX ReadOnly mode on an existing Kubernetes Cluster, run the following commands

This MLX ReadOnly mode only contains MLX ReadOnly deployment.

```shell
git clone https://github.com/machine-learning-exchange/mlx
cd mlx
kubectl apply -k manifests/read-only-k8s
```

To delete the read-only deployment, run
```
kubectl delete -k manifests/read-only-k8s
```
