# Install Operator Manually

1. Clone Kubeflow Operator repository, build the manifests and install the Operator

    ```shell
    git clone https://github.com/kubeflow/kfctl.git && cd kfctl

    ```

    Create the namespace for the Operator:
    ```
    export OPERATOR_NAMESPACE=operators
    kubectl create ns ${OPERATOR_NAMESPACE}
    ```

    Update the namespace in the manifests:
    ```
    cd deploy/
    kustomize edit set namespace ${OPERATOR_NAMESPACE}
    ```

    Install the Operator
    ```
    kustomize build | sed 's/kubeflow-operator$/mlx-operator/' | kubectl apply -f -
    ```

2. Deploy MLX

    Now you can apply MLX [_KfDef_](https://www.kubeflow.org/docs/distributions/operator/introduction/#kubeflow-operator) custom resource on Kubernetes to deploy MLX.

    For IKS / Minikube use the following KFDEF
    ```shell
    export KFDEF_URL=https://raw.githubusercontent.com/machine-learning-exchange/manifests/mlx/kfdef/kfctl_ibm_tekton.yaml
    ```

    For Openshift we need to set the proper scc. Use the following KFDEF
    ```shell
    export KFDEF_URL=https://raw.githubusercontent.com/machine-learning-exchange/manifests/mlx/kfdef/kfctl_mlx_openshift_tekton.yaml
    ```

    Download the KFDEF to local:
    ```shell
    export KFDEF=$(echo "${KFDEF_URL}" | rev | cut -d/ -f1 | rev)
    curl -L ${KFDEF_URL} > ${KFDEF}
    ```

    Use `kfctl` to deploy MLX
    ```shell
    kubectl create ns kubeflow
    # add metadata.name field
    # Note: yq can be installed from https://github.com/mikefarah/yq/releases/
    # Please use yq v4+
    export KUBEFLOW_DEPLOYMENT_NAME=kubeflow
    yq eval --inplace ".metadata.name = \"$KUBEFLOW_DEPLOYMENT_NAME\"" "$KFDEF"
    kfctl apply -V -f "${KFDEF}"
    ```

3. (Optional) Enable development mode
    When developing with MLX, we recommend to run the below command to disable monitoring from the operator framework
    ```shell
    kubectl patch deployment mlx-operator -n operators -p '{"spec":{"replicas":0}}'
    ```

[Back To Home](../README.md)
