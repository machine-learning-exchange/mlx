1. run `python icp4d-demo-pipeline.py` to compile the pipeline
2. go to KFP and upload the tar file.

Note: The below code block is the default external ip for the demo cluster. Update the creds by running the below code in jupyterlab if this demo is presented in a different cluster.
```
import requests
import subprocess
res = requests.get('https://storage.googleapis.com/kubernetes-release/release/v1.14.0/bin/linux/amd64/kubectl', allow_redirects=True)
open('kubectl', 'wb').write(res.content)
subprocess.call(['chmod', '755', 'kubectl'])

e2e_creds= {
    'local_cluster_deployment': 'true',
    'public_ip': '169.45.69.227'
}

### Define a secret_name for your credentials
secret_name_e2e = "icp4d-demo"
command = ['./kubectl', 'create', 'secret', 'generic', secret_name_e2e]
for key in e2e_creds:
    command.append('--from-literal=%s=\'%s\'' % (key, e2e_creds[key]))
    
!./kubectl delete secret $secret_name_e2e

subprocess.run(command)

!./kubectl describe secret $secret_name_e2e
```
