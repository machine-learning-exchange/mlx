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

- **CPUs**: 8 Cores
- **Memory**: 16 GB RAM
- **Disk**: 32+ GB

**Note**: We found that on older laptops, like a 2016 MacBook Pro (2.7 GHz i7, 16 GB RAM) the MLX
deployment on KIND may require to give all available resources to the Docker daemon in order to be
able to deploy the manifests and run basic pipelines. Even then, trying to run notebooks or deploying 
a model, will cause the laptop to get very slow with fans running full throttle. It may even cause
other application to crash.


## Create KIND Cluster

```Bash
kind create cluster --name mlx --image kindest/node:v1.21.12
kubectl cluster-info --context kind-mlx
kubectl get pods --all-namespaces
```


## Deploy MLX (Single-User)

```Bash
git clone https://github.com/IBM/manifests -b v1.4.0-mlx
cd manifests

# run the below command two times if the CRDs take too long to provision
while ! kustomize build mlx-single-kind | \
  kubectl apply -f -; do echo "Retrying to apply resources"; sleep 10; done

# wait while the MLX deployment is starting up, may take 10 to 20 minutes
while $( kubectl get pods --all-namespaces | grep -q -v "STATUS\|Running" ); do \
  echo "Hold tight, still waiting for $( kubectl get pods --all-namespaces | grep -v "STATUS\|Running" | wc -l ) pods ..."; \
  sleep 10; \
done

# check pod status
kubectl get pods --all-namespaces

# make the MLX UI available to your local browser on http://localhost:3000/
kubectl port-forward -n istio-system svc/istio-ingressgateway 3000:80 &
```

Now paste the URL http://localhost:3000/login into your browser and proceed to
[import the MLX catalog](import-assets.md), or, upload the assets from the
[default MLX asset catalog](https://github.com/machine-learning-exchange/katalog)
using the MLX API directly with `curl`:

```Bash
UPLOAD_API="http://localhost:3000/apis/v1alpha1/catalog/upload_from_url"
CATALOG_URL="https://raw.githubusercontent.com/machine-learning-exchange/mlx/main/bootstrapper/catalog_upload.json"

curl -X POST \
    -H "Content-Type: multipart/form-data" \
    -F url="${CATALOG_URL}" \
    -s "${UPLOAD_API}" | grep -iE "total_|error"
```

Delete the `mlx` cluster when it is no longer needed:

```Bash
kind delete cluster --name mlx
```


## Install Kubeflow Pipelines (for Reference only, Optional)

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

