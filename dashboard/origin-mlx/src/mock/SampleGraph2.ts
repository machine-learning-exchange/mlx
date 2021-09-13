// Copyright 2021 IBM Corporation
// 
// SPDX-License-Identifier: Apache-2.0
const SAMPLE_GRAPH = 
`apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: model-deployment-pipeline-
spec:
  arguments:
    parameters:
    - name: model-id
      value: max-image-caption-generator
  entrypoint: model-deployment-pipeline
  serviceAccountName: pipeline-runner
  templates:
  - container:
      args:
      - -u
      - kube_deployment.py
      - --model_serving_image
      - '{{inputs.parameters.model-config-model-serving-image}}'
      - --deployment_name
      - '{{inputs.parameters.model-config-deployment-name}}'
      command:
      - python
      image: aipipeline/k8s-model-deploy
      volumeMounts:
      - mountPath: /app/secrets
        name: e2e-creds
    inputs:
      parameters:
      - name: model-config-deployment-name
      - name: model-config-model-serving-image
    name: k8s-model-deployment
    outputs:
      artifacts:
      - name: mlpipeline-ui-metadata
        path: /mlpipeline-ui-metadata.json
        s3:
          accessKeySecret:
            key: accesskey
            name: mlpipeline-minio-artifact
          bucket: mlpipeline
          endpoint: minio-service.kubeflow:9000
          insecure: true
          key: runs/{{workflow.uid}}/{{pod.name}}/mlpipeline-ui-metadata.tgz
          secretKeySecret:
            key: secretkey
            name: mlpipeline-minio-artifact
      - name: mlpipeline-metrics
        path: /mlpipeline-metrics.json
        s3:
          accessKeySecret:
            key: accesskey
            name: mlpipeline-minio-artifact
          bucket: mlpipeline
          endpoint: minio-service.kubeflow:9000
          insecure: true
          key: runs/{{workflow.uid}}/{{pod.name}}/mlpipeline-metrics.tgz
          secretKeySecret:
            key: secretkey
            name: mlpipeline-minio-artifact
      parameters:
      - name: k8s-model-deployment-output
        valueFrom:
          path: /tmp/log.txt
  - container:
      args:
      - -u
      - model-config.py
      - --secret_name
      - e2e-creds
      - --model_id
      - '{{inputs.parameters.model-id}}'
      command:
      - python
      image: tomcli/model-config
    inputs:
      parameters:
      - name: model-id
    name: model-config
    outputs:
      artifacts:
      - name: mlpipeline-ui-metadata
        path: /mlpipeline-ui-metadata.json
        s3:
          accessKeySecret:
            key: accesskey
            name: mlpipeline-minio-artifact
          bucket: mlpipeline
          endpoint: minio-service.kubeflow:9000
          insecure: true
          key: runs/{{workflow.uid}}/{{pod.name}}/mlpipeline-ui-metadata.tgz
          secretKeySecret:
            key: secretkey
            name: mlpipeline-minio-artifact
      - name: mlpipeline-metrics
        path: /mlpipeline-metrics.json
        s3:
          accessKeySecret:
            key: accesskey
            name: mlpipeline-minio-artifact
          bucket: mlpipeline
          endpoint: minio-service.kubeflow:9000
          insecure: true
          key: runs/{{workflow.uid}}/{{pod.name}}/mlpipeline-metrics.tgz
          secretKeySecret:
            key: secretkey
            name: mlpipeline-minio-artifact
      parameters:
      - name: model-config-deployment-name
        valueFrom:
          path: /tmp/deployment_name
      - name: model-config-model-serving-image
        valueFrom:
          path: /tmp/model_serving_image
  - dag:
      tasks:
      - arguments:
          parameters:
          - name: model-config-deployment-name
            value: '{{tasks.model-config.outputs.parameters.model-config-deployment-name}}'
          - name: model-config-model-serving-image
            value: '{{tasks.model-config.outputs.parameters.model-config-model-serving-image}}'
        dependencies:
        - model-config
        name: k8s-model-deployment
        template: k8s-model-deployment
      - arguments:
          parameters:
          - name: model-id
            value: '{{inputs.parameters.model-id}}'
        name: model-config
        template: model-config
    inputs:
      parameters:
      - name: model-id
    name: model-deployment-pipeline
  volumes:
  - name: e2e-creds
    secret:
      secretName: e2e-creds`

  export default SAMPLE_GRAPH;
