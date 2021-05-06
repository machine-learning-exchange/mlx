# Install Operator Manually

1. Clone Kubeflow Operator repository, build the manifests and install the Operator

```shell
git clone https://github.com/kubeflow/kfctl.git && cd kfctl

export OPERATOR_NAMESPACE=operators
kubectl create ns ${OPERATOR_NAMESPACE}

cd deploy/
kustomize edit set namespace ${OPERATOR_NAMESPACE}
# kustomize edit add resource kustomize/include/quota # only deploy this if the k8s cluster is 1.15+ and has resource quota support, which will allow only one _kfdef_ instance or one deployment of Kubeflow on the cluster. This follows the singleton model, and is the current recommended and supported mode.

kustomize build | sed 's/kubeflow-operator/mlx-operator/' | kubectl apply -f -
```

2. Deploy MLX

Now you can apply MLX [_KfDef_](https://www.kubeflow.org/docs/distributions/operator/introduction/#kubeflow-operator) custom resource on Kubernetes to deploy MLX.

For IKS / Minikube use the following KFDEF
```shell
export KFDEF=https://raw.githubusercontent.com/machine-learning-exchange/manifests/mlx/kfdef/kfctl_ibm_tekton.yaml
```

For Openshift we need to set the proper scc. Use the following KFDEF
```shell
export KFDEF_URL=https://raw.githubusercontent.com/machine-learning-exchange/manifests/mlx/kfdef/kfctl_mlx_openshift_tekton.yaml
export KFDEF=$(echo "${KFDEF_URL}" | rev | cut -d/ -f1 | rev)
curl -L ${KFDEF_URL} > ${KFDEF}
```

```shell
kubectl create ns kubeflow
# add metadata.name field
# Note: yq can be installed from https://github.com/mikefarah/yq
export KUBEFLOW_DEPLOYMENT_NAME=kubeflow
# on yq version <4 
yq w ${KFDEF} 'metadata.name' ${KUBEFLOW_DEPLOYMENT_NAME} > ${KFDEF}.tmp && mv ${KFDEF}.tmp ${KFDEF}
# on yq version 4+
yq e ".metadata.name = \"$KUBEFLOW_DEPLOYMENT_NAME\"" kfctl_mlx_openshift_tekton.yaml > $KFDEF.tmp && mv $KFDEF.tmp $KFDEF
kfctl apply -V -f ${KFDEF}
```

3. (Optional) Enable development mode
When developing with MLX, we recommend to run the below command to disable monitoring from the operator framework
```shell
kubectl patch deployment kubeflow-operator -n operators -p '{"spec":{"replicas":0}}'
```

[Back To Home](../README.md)
