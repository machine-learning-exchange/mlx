# How to use it
1. Install MLX
2. Get the [github.ibm.com personal access token](https://github.ibm.com/settings/tokens/new) and give it access to read all public repos.
3. Fillin the below environment variables in [bootstrap.yaml](bootstrap.yaml):
   - **enterprise_github_token**: github.ibm.com personal access token from step 2.
4. Deploy boostrapper:
   ```shell
   kubectl apply -f bootstrapper/bootstrap.yaml -n kubeflow
   kubectl apply -f bootstrapper/configmap.yaml -n kubeflow 
   ```
   
   After 2-5 minutes, the assets in [configmap.yaml](configmap.yaml) should be populated.
