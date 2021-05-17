# Deploy MLX on an Existing Kubeflow Cluster

To deploy MLX on an existing Kubeflow Cluster, we can simply use the kustomize plugin that comes with `kubectl` client on v1.17+. Clone the [MLX](https://github.com/machine-learning-exchange/mlx) repo and run the following commands based on your Kubeflow setup.

```shell
git clone https://github.com/machine-learning-exchange/mlx
cd mlx
```

-  Deploy MLX on Single User Kubeflow (Without OIDC Auth)
```shell
kubectl apply -k manifests/base
```

- Deploy MLX on Multi-User Kubeflow (With OIDC and Istio Mutual Auth)
```shell
kubectl apply -k manifests/multi-user
```

Then access the MLX page using `http://<Kubeflow_Endpoint>/os/`
