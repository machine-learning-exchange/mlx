// Copyright 2021 IBM Corporation 
// 
// SPDX-License-Identifier: Apache-2.0
const SAMPLE_GRAPH = 
`apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: ffdl-pipeline-
spec:
  arguments:
    parameters:
    - name: model-def-file-path
      value: gender_classification_training.zip
    - name: manifest-file-path
      value: manifest_training.yml
    - name: preprocessing-def-file-path
      value: preprocessing.zip
    - name: preprocessing-manifest-file-path
      value: preprocessing_manifest.yml
    - name: fgsm-attack-epsilon
      value: '0.2'
    - name: primary-model-revision
      value: model-serving-00001
    - name: new-model-traffic-percentage
      value: '5'
    - name: model-class-file
      value: gender_classification_training.py
    - name: model-class-name
      value: ThreeLayerCNN
    - name: loss-fn
      value: torch.nn.CrossEntropyLoss()
    - name: optimizer
      value: torch.optim.Adam(model.parameters(), lr=0.001)
    - name: clip-values
      value: (0, 1)
    - name: nb-classes
      value: '2'
    - name: input-shape
      value: (1,3,64,64)
    - name: feature-testset-path
      value: processed_data/X_test.npy
    - name: label-testset-path
      value: processed_data/y_test.npy
    - name: protected-label-testset-path
      value: processed_data/p_test.npy
    - name: favorable-label
      value: '0.0'
    - name: unfavorable-label
      value: '1.0'
    - name: privileged-groups
      value: '[{''race'': 0.0}]'
    - name: unprivileged-groups
      value: '[{''race'': 4.0}]'
    - name: namespace
      value: serving
  entrypoint: ffdl-pipeline
  onExit: exit-handler
  serviceAccountName: pipeline-runner
  templates:
  - container:
      args:
      - python -u train.py --model_def_file_path {{inputs.parameters.preprocessing-def-file-path}}
        --manifest_file_path {{inputs.parameters.preprocessing-manifest-file-path}};
      command:
      - sh
      - -c
      image: aipipeline/ffdl-train
      volumeMounts:
      - mountPath: /app/secrets
        name: e2e-creds
    inputs:
      parameters:
      - name: preprocessing-def-file-path
      - name: preprocessing-manifest-file-path
    name: data-preprocessing
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
      - name: data-preprocessing-output
        valueFrom:
          path: /tmp/training_id.txt
  - container:
      args:
      - 'curl -X POST -H ''Content-type: application/json'' --data ''{"text":"KubeFlow
        Pipeline Run for {{workflow.name}} is {{workflow.status}}"}'' $(cat /app/secrets/slack_api_endpoint
        | tr -d "''")'
      command:
      - sh
      - -c
      image: aipipeline/util
      volumeMounts:
      - mountPath: /app/secrets
        name: e2e-creds
    name: exit-handler
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
  - dag:
      tasks:
      - arguments:
          parameters:
          - name: preprocessing-def-file-path
            value: '{{inputs.parameters.preprocessing-def-file-path}}'
          - name: preprocessing-manifest-file-path
            value: '{{inputs.parameters.preprocessing-manifest-file-path}}'
        name: data-preprocessing
        template: data-preprocessing
      - arguments:
          parameters:
          - name: favorable-label
            value: '{{inputs.parameters.favorable-label}}'
          - name: feature-testset-path
            value: '{{inputs.parameters.feature-testset-path}}'
          - name: ffdl-training-output
            value: '{{tasks.ffdl-training.outputs.parameters.ffdl-training-output}}'
          - name: label-testset-path
            value: '{{inputs.parameters.label-testset-path}}'
          - name: model-class-file
            value: '{{inputs.parameters.model-class-file}}'
          - name: model-class-name
            value: '{{inputs.parameters.model-class-name}}'
          - name: privileged-groups
            value: '{{inputs.parameters.privileged-groups}}'
          - name: protected-label-testset-path
            value: '{{inputs.parameters.protected-label-testset-path}}'
          - name: unfavorable-label
            value: '{{inputs.parameters.unfavorable-label}}'
          - name: unprivileged-groups
            value: '{{inputs.parameters.unprivileged-groups}}'
        dependencies:
        - ffdl-training
        name: fairness-check
        template: fairness-check
      - arguments:
          parameters:
          - name: data-preprocessing-output
            value: '{{tasks.data-preprocessing.outputs.parameters.data-preprocessing-output}}'
          - name: manifest-file-path
            value: '{{inputs.parameters.manifest-file-path}}'
          - name: model-def-file-path
            value: '{{inputs.parameters.model-def-file-path}}'
        dependencies:
        - data-preprocessing
        name: ffdl-training
        template: ffdl-training
      - arguments:
          parameters:
          - name: model-class-file
            value: '{{inputs.parameters.model-class-file}}'
          - name: model-class-name
            value: '{{inputs.parameters.model-class-name}}'
          - name: namespace
            value: '{{inputs.parameters.namespace}}'
          - name: new-model-traffic-percentage
            value: '{{inputs.parameters.new-model-traffic-percentage}}'
          - name: primary-model-revision
            value: '{{inputs.parameters.primary-model-revision}}'
          - name: robustness-check-training-id
            value: '{{tasks.robustness-check.outputs.parameters.robustness-check-training-id}}'
        dependencies:
        - robustness-check
        name: model-deployment
        template: model-deployment
      - arguments:
          parameters:
          - name: clip-values
            value: '{{inputs.parameters.clip-values}}'
          - name: feature-testset-path
            value: '{{inputs.parameters.feature-testset-path}}'
          - name: ffdl-training-output
            value: '{{tasks.ffdl-training.outputs.parameters.ffdl-training-output}}'
          - name: fgsm-attack-epsilon
            value: '{{inputs.parameters.fgsm-attack-epsilon}}'
          - name: input-shape
            value: '{{inputs.parameters.input-shape}}'
          - name: label-testset-path
            value: '{{inputs.parameters.label-testset-path}}'
          - name: loss-fn
            value: '{{inputs.parameters.loss-fn}}'
          - name: model-class-file
            value: '{{inputs.parameters.model-class-file}}'
          - name: model-class-name
            value: '{{inputs.parameters.model-class-name}}'
          - name: nb-classes
            value: '{{inputs.parameters.nb-classes}}'
          - name: optimizer
            value: '{{inputs.parameters.optimizer}}'
        dependencies:
        - ffdl-training
        name: robustness-check
        template: robustness-check
    inputs:
      parameters:
      - name: clip-values
      - name: favorable-label
      - name: feature-testset-path
      - name: fgsm-attack-epsilon
      - name: input-shape
      - name: label-testset-path
      - name: loss-fn
      - name: manifest-file-path
      - name: model-class-file
      - name: model-class-name
      - name: model-def-file-path
      - name: namespace
      - name: nb-classes
      - name: new-model-traffic-percentage
      - name: optimizer
      - name: preprocessing-def-file-path
      - name: preprocessing-manifest-file-path
      - name: primary-model-revision
      - name: privileged-groups
      - name: protected-label-testset-path
      - name: unfavorable-label
      - name: unprivileged-groups
    name: exit-handler-1
  - container:
      args:
      - python -u fairness_check.py --model_id {{inputs.parameters.ffdl-training-output}}
        --model_class_file {{inputs.parameters.model-class-file}} --model_class_name
        {{inputs.parameters.model-class-name}} --favorable_label {{inputs.parameters.favorable-label}}
        --unfavorable_label {{inputs.parameters.unfavorable-label}} --feature_testset_path
        {{inputs.parameters.feature-testset-path}} --label_testset_path {{inputs.parameters.label-testset-path}}
        --protected_label_testset_path {{inputs.parameters.protected-label-testset-path}}
        --privileged_groups "{{inputs.parameters.privileged-groups}}" --unprivileged_groups
        "{{inputs.parameters.unprivileged-groups}}";echo {{inputs.parameters.ffdl-training-output}}
        > /tmp/training-id.txt;
      command:
      - sh
      - -c
      image: aipipeline/fairness-check-with-secret:pytorch-v3
      volumeMounts:
      - mountPath: /app/secrets
        name: e2e-creds
    inputs:
      parameters:
      - name: favorable-label
      - name: feature-testset-path
      - name: ffdl-training-output
      - name: label-testset-path
      - name: model-class-file
      - name: model-class-name
      - name: privileged-groups
      - name: protected-label-testset-path
      - name: unfavorable-label
      - name: unprivileged-groups
    name: fairness-check
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
      - name: fairness-check-output
        valueFrom:
          path: /tmp/fairness.txt
      - name: fairness-check-training-id
        valueFrom:
          path: /tmp/training-id.txt
  - dag:
      tasks:
      - arguments:
          parameters:
          - name: clip-values
            value: '{{inputs.parameters.clip-values}}'
          - name: favorable-label
            value: '{{inputs.parameters.favorable-label}}'
          - name: feature-testset-path
            value: '{{inputs.parameters.feature-testset-path}}'
          - name: fgsm-attack-epsilon
            value: '{{inputs.parameters.fgsm-attack-epsilon}}'
          - name: input-shape
            value: '{{inputs.parameters.input-shape}}'
          - name: label-testset-path
            value: '{{inputs.parameters.label-testset-path}}'
          - name: loss-fn
            value: '{{inputs.parameters.loss-fn}}'
          - name: manifest-file-path
            value: '{{inputs.parameters.manifest-file-path}}'
          - name: model-class-file
            value: '{{inputs.parameters.model-class-file}}'
          - name: model-class-name
            value: '{{inputs.parameters.model-class-name}}'
          - name: model-def-file-path
            value: '{{inputs.parameters.model-def-file-path}}'
          - name: namespace
            value: '{{inputs.parameters.namespace}}'
          - name: nb-classes
            value: '{{inputs.parameters.nb-classes}}'
          - name: new-model-traffic-percentage
            value: '{{inputs.parameters.new-model-traffic-percentage}}'
          - name: optimizer
            value: '{{inputs.parameters.optimizer}}'
          - name: preprocessing-def-file-path
            value: '{{inputs.parameters.preprocessing-def-file-path}}'
          - name: preprocessing-manifest-file-path
            value: '{{inputs.parameters.preprocessing-manifest-file-path}}'
          - name: primary-model-revision
            value: '{{inputs.parameters.primary-model-revision}}'
          - name: privileged-groups
            value: '{{inputs.parameters.privileged-groups}}'
          - name: protected-label-testset-path
            value: '{{inputs.parameters.protected-label-testset-path}}'
          - name: unfavorable-label
            value: '{{inputs.parameters.unfavorable-label}}'
          - name: unprivileged-groups
            value: '{{inputs.parameters.unprivileged-groups}}'
        name: exit-handler-1
        template: exit-handler-1
    inputs:
      parameters:
      - name: clip-values
      - name: favorable-label
      - name: feature-testset-path
      - name: fgsm-attack-epsilon
      - name: input-shape
      - name: label-testset-path
      - name: loss-fn
      - name: manifest-file-path
      - name: model-class-file
      - name: model-class-name
      - name: model-def-file-path
      - name: namespace
      - name: nb-classes
      - name: new-model-traffic-percentage
      - name: optimizer
      - name: preprocessing-def-file-path
      - name: preprocessing-manifest-file-path
      - name: primary-model-revision
      - name: privileged-groups
      - name: protected-label-testset-path
      - name: unfavorable-label
      - name: unprivileged-groups
    name: ffdl-pipeline
  - container:
      args:
      - echo preprocessing ID for this model is {{inputs.parameters.data-preprocessing-output}};
        python -u train.py --model_def_file_path {{inputs.parameters.model-def-file-path}}
        --manifest_file_path {{inputs.parameters.manifest-file-path}};
      command:
      - sh
      - -c
      image: aipipeline/ffdl-train
      volumeMounts:
      - mountPath: /app/secrets
        name: e2e-creds
    inputs:
      parameters:
      - name: data-preprocessing-output
      - name: manifest-file-path
      - name: model-def-file-path
    name: ffdl-training
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
      - name: ffdl-training-output
        valueFrom:
          path: /tmp/training_id.txt
  - container:
      args:
      - python -u knative_deployment.py --model_id {{inputs.parameters.robustness-check-training-id}}
        --primary_model_revision {{inputs.parameters.primary-model-revision}} --traffic_percentage
        {{inputs.parameters.new-model-traffic-percentage}} --metric_path /tmp/log.txt
        --model_class_name {{inputs.parameters.model-class-name}} --model_class_file
        {{inputs.parameters.model-class-file}} --model_serving_image tomcli/knative-serving:pytorch
        --namespace {{inputs.parameters.namespace}}; echo model {{inputs.parameters.robustness-check-training-id}}
        is deployed.;
      command:
      - sh
      - -c
      image: aipipeline/deployment-knative-remote
      volumeMounts:
      - mountPath: /app/secrets
        name: e2e-creds
    inputs:
      parameters:
      - name: model-class-file
      - name: model-class-name
      - name: namespace
      - name: new-model-traffic-percentage
      - name: primary-model-revision
      - name: robustness-check-training-id
    name: model-deployment
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
      - name: model-deployment-output
        valueFrom:
          path: /tmp/log.txt
  - container:
      args:
      - python -u robustness_check.py --model_id {{inputs.parameters.ffdl-training-output}}
        --epsilon {{inputs.parameters.fgsm-attack-epsilon}} --model_class_file {{inputs.parameters.model-class-file}}
        --model_class_name {{inputs.parameters.model-class-name}} --loss_fn "{{inputs.parameters.loss-fn}}"
        --optimizer "{{inputs.parameters.optimizer}}" --clip_values "{{inputs.parameters.clip-values}}"
        --nb_classes {{inputs.parameters.nb-classes}} --input_shape "{{inputs.parameters.input-shape}}"
        --feature_testset_path {{inputs.parameters.feature-testset-path}} --label_testset_path
        {{inputs.parameters.label-testset-path}};echo {{inputs.parameters.ffdl-training-output}}
        > /tmp/training-id.txt;
      command:
      - sh
      - -c
      image: aipipeline/robustness-check-with-secret:pytorch-v2
      volumeMounts:
      - mountPath: /app/secrets
        name: e2e-creds
    inputs:
      parameters:
      - name: clip-values
      - name: feature-testset-path
      - name: ffdl-training-output
      - name: fgsm-attack-epsilon
      - name: input-shape
      - name: label-testset-path
      - name: loss-fn
      - name: model-class-file
      - name: model-class-name
      - name: nb-classes
      - name: optimizer
    name: robustness-check
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
      - name: robustness-check-output
        valueFrom:
          path: /tmp/robustness.txt
      - name: robustness-check-robust
        valueFrom:
          path: /tmp/status.txt
      - name: robustness-check-training-id
        valueFrom:
          path: /tmp/training-id.txt
  volumes:
  - name: e2e-creds
  secret:
  secretName: e2e-creds`

  export default SAMPLE_GRAPH;
