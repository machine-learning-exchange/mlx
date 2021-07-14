## Troubleshooting

* When deleting the Kubeflow deployment, some _mutatingwebhookconfigurations_ resources are cluster-wide resources and may not be removed as their owner is not the _KfDef_ instance. To remove them, run following:

	```shell
	kubectl delete mutatingwebhookconfigurations admission-webhook-mutating-webhook-configuration
	kubectl delete mutatingwebhookconfigurations inferenceservice.serving.kubeflow.org
	kubectl delete mutatingwebhookconfigurations istio-sidecar-injector
	kubectl delete mutatingwebhookconfigurations katib-mutating-webhook-config
	kubectl delete mutatingwebhookconfigurations mutating-webhook-configurations
	kubectl delete mutatingwebhookconfigurations cache-webhook-kubeflow
	```

* If you don't see any sample pipeline or receive `Failed to establish a new connection` messages. It's because IBM Cloud NFS storage might be taking too long to provision which makes the storage and backend microservices timed out. In this case, you have to run the below commands to restart the pods.
	```shell
	# Replace kubeflow with the KFP namespace
	NAMESPACE=kubeflow
	kubectl get pods -n ${NAMESPACE:-kubeflow}
	kubectl delete pod -n ${NAMESPACE:-kubeflow} $(kubectl get pods -n ${NAMESPACE:-kubeflow} -l app=ml-pipeline | grep ml-pipeline | awk '{print $1;exit}')
	kubectl delete pod -n ${NAMESPACE:-kubeflow} $(kubectl get pods -n ${NAMESPACE:-kubeflow} -l app=ml-pipeline-persistenceagent | grep ml-pipeline | awk '{print $1;exit}')
	kubectl delete pod -n ${NAMESPACE:-kubeflow} $(kubectl get pods -n ${NAMESPACE:-kubeflow} -l app=ml-pipeline-ui | grep ml-pipeline | awk '{print $1;exit}')
	kubectl delete pod -n ${NAMESPACE:-kubeflow} $(kubectl get pods -n ${NAMESPACE:-kubeflow} -l app=ml-pipeline-scheduledworkflow | grep ml-pipeline | awk '{print $1;exit}')
	```
	Then you can redeploy the bootstrapper to properly populate the default assets. Remember to insert the IBM Github Token if you want to retrieve any asset within IBM Github.
	```shell
	vim bootstrapper/bootstrap.yaml # Insert the IBM Github Token
	kubectl delete -f bootstrapper/bootstrap.yaml -n $NAMESPACE
	kubectl apply -f bootstrapper/bootstrap.yaml -n $NAMESPACE
	```

* Additional troubleshooting on IBM Cloud is available at [the wiki page](https://github.com/machine-learning-exchange/mlx/wiki/Troubleshooting).
