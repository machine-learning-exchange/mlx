# Deploy MLX on an Existing Kubeflow Cluster

This is a complete deployment of MLX which includes all of the following components:

- [Istio](https://istio.io/) (with [mutual TLS](https://istio.io/latest/docs/tasks/security/authentication/authn-policy/#auto-mutual-tls))
- [Kubeflow Pipelines](https://www.kubeflow.org/docs/components/pipelines/), in [Multi-User mode](https://www.kubeflow.org/docs/components/pipelines/multi-user/)
- [Tekton Pipelines](https://github.com/tektoncd/pipeline#-tekton-pipelines)
- [Datashim](https://datashim-io.github.io/datashim/) to provide access to S3 and NFS Datasets within pods
- [KFServing](https://www.kubeflow.org/docs/components/kfserving/kfserving/) for model deployment
- MLX API and UI

To deploy MLX on a Kubernetes cluster which has Kubeflow 1.3.0 already installed, we use the kustomize plugin that comes with `kubectl` client v1.17+. Clone the [MLX](https://github.com/machine-learning-exchange/mlx) repo and run the following commands based on your Kubeflow setup.

```shell
git clone https://github.com/machine-learning-exchange/mlx
cd mlx
```

- Deploy MLX on Kubeflow (With OIDC and Istio Mutual Auth)
```shell
kubectl apply -k manifests/istio-auth
```

Then access the MLX page using `http://<Kubeflow_Endpoint>/mlx/`


## Replacing Kubeflow Central Dashboard with MLX Dashboard

To deploy MLX on Kubeflow (With OIDC and Istio Mutual Auth) and replace Kubeflow Central Dashboard with MLX Dashboard, run the following commands:

```shell
git clone https://github.com/machine-learning-exchange/mlx
cd mlx
```

- Deploy MLX on Kubeflow (With OIDC and Istio Mutual Auth)
```shell
kubectl apply -k manifests/prod-multi-user
```

Then access the MLX page using `http://<Kubeflow_Endpoint>/`
