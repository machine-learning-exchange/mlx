# Deploy MLX on KIND

Kubernetes in Docker (KIND) provides an easy way to deploy MLX locally including
Kubeflow Pipelines which makes it possible to run generated sample pipelines for
any of the registered MLX assets.

## Installation

- [Docker](https://docs.docker.com/desktop/#download-and-install)
- [Homebrew](https://brew.sh/) (on macOS)
- [Kustomize](https://kubectl.docs.kubernetes.io/installation/kustomize/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)
- [KIND](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)


### Install Required CLIs (macOS)

After installing Docker and Homebrew (linked above) you can install the `kind`,
`kustomize`, and `kubectl` CLIs with `brew install`. For Windows and Linux follow
the respective home pages for installation instructions.

```Bash
brew install kind
kind --version

brew install kubectl
kubectl version --client

brew install kustomize
kustomize version
```

**Note:** We successfully tested this KIND deployment with the latest version of `kustomize` `v4.4.0`.
However, there have been issues in the past with versions later then `v3.2.0`. To be on the safe side
you could download the `kustomize` `v3.2.0` binary as described
[here](https://www.kubeflow.org/docs/distributions/ibm/deploy/deployment-process/#install-kubectl-and-kustomize)


## Docker Resources

Increase the default resources for Docker:

- CPUs: 4 Cores
- Memory: 8 GB RAM
- Disk: 32+ GB

**Note**: We found that on older laptops, like a 2016 15 in MacBook Pro (2.7 GHz i7, 16 GB) the MLX
deployment on KIND may require to give all available resources to the Docker daemon in order to be
able to deploy the manifests and run basic pipelines. Even then, trying to run notebooks or deploying 
a model, will cause the laptop to get very slow with fans running full throttle. It may even cause
other application to crash.


## Create KIND Cluster

```Bash
kind create cluster --name mlx
kubectl cluster-info --context kind-mlx
kubectl get pods --all-namespaces
```


## Deploy MLX (Single-User)

```Bash
git clone https://github.com/IBM/manifests -b v1.4.0-mlx
cd manifests

# run the below command two times if the CRDs take too long to provision.
while ! kustomize build mlx-single | \
  kubectl apply -f -; do echo "Retrying to apply resources"; sleep 10; done

# check pod status
kubectl get pods --all-namespaces

# make the MLX UI available to your local browser on http://localhost:3000/
kubectl port-forward -n istio-system svc/istio-ingressgateway 3000:80
```

Now paste the URL http://localhost:3000/ into your browser and proceed to
[import the MLX catalog](import-assets.md).

Delete the `mlx` cluster when it is no longer needed:

```Bash
kind delete cluster --name mlx
```


## Install Kubeflow Pipelines (for reference, optional)

```Bash
kind create cluster --name kfp
kubectl cluster-info --context kind-kfp

# env/platform-agnostic-pns hasn't been publically released, so you will install it from master
export PIPELINE_VERSION=1.7.1
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic-pns?ref=$PIPELINE_VERSION"

kubectl get pods --all-namespaces

# make the Kubeflow Pipelines UI available on http://localhost:8080/#/pipelines
kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80

kind delete cluster --name kfp
```

