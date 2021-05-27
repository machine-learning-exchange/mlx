## Install Kfctl

**Note**: kfctl is currently available for Linux and macOS users only. If you use Windows, you can install kfctl on Windows Subsystem for Linux (WSL). Refer to the official [instructions](https://docs.microsoft.com/en-us/windows/wsl/install-win10) for setting up WSL.

Run the following commands to set up and deploy Kubeflow:

1. Download the latest kfctl {{% kf-latest-version %}} release from the
  [Kubeflow releases 
  page](https://github.com/kubeflow/kfctl/releases/tag/{{% kf-latest-version %}}).
  
  **Note**: You're strongly recommended to install **kfctl v1.2** or above because kfctl v1.2 addresses several critical bugs that can break the Kubeflow deployment.

2. Extract the archived TAR file:

      ```shell
      tar -xvf kfctl_{{% kf-latest-version %}}_<platform>.tar.gz
      ```
3. Make kfctl binary easier to use (optional). If you don’t add the binary to your path, you must use the full path to the kfctl binary each time you run it.

      ```shell
      export PATH=$PATH:<path to where kfctl was unpacked>
      ```


## Deploy MLX

1. Now you can apply MLX [_KfDef_](https://www.kubeflow.org/docs/distributions/operator/introduction/#kubeflow-operator) custom resource on Kubernetes to deploy MLX.

2. For IKS / Minikube use the following KFDEF
    ```shell
    export KFDEF_URL=https://raw.githubusercontent.com/machine-learning-exchange/manifests/mlx/kfdef/kfctl_ibm_tekton.yaml
    ```

    **OR**

    For Openshift we need to set the proper scc. Use the following KFDEF
    ```shell
    export KFDEF_URL=https://raw.githubusercontent.com/machine-learning-exchange/manifests/mlx/kfdef/kfctl_mlx_openshift_tekton.yaml
    ```

3. Download the KFDEF to local:
    ```shell
    export KFDEF=$(echo "${KFDEF_URL}" | rev | cut -d/ -f1 | rev)
    curl -L ${KFDEF_URL} > ${KFDEF}
    ```

4. Use `kfctl` to deploy MLX
    ```shell
    kfctl apply -V -f ${KFDEF}
    ```

[Back To Home](../README.md)
