// Copyright 2021 IBM Corporation
// 
// SPDX-License-Identifier: Apache-2.0
export const FFDLData =
`apiVersion: operators.coreos.com/v1alpha1
kind: ClusterServiceVersion
metadata:
  name: ffdl-operator.v0.0.1
  namespace: placeholder
  annotations:
    capabilities: "Basic Install"
    categories: "AI/Machine Learning"
    description: "Fabric for Deep Learning - an operating system fabric for Deep Learning"
    containerImage: docker.io/ffdlops/ffdl:v0.0.1
    support: IBM
    certified: "false"
    createdAt: 2019-04-24T08:00:00Z
    alm-examples: |-
      [
        {
          "apiVersion": "mlx.com/v1alpha1",
          "kind": "FfDL",
          "metadata": {
            "name": "ffdl-cr"
          },
          "spec": {
            "replicaCount": 1,
            "image": {
              "repository": "nginx",
              "tag": "stable",
              "pullPolicy": "IfNotPresent"
            },
            "nameOverride": "",
            "fullnameOverride": "",
            "service": {
              "type": "ClusterIP",
              "port": 80
            },
            "ingress": {
              "enabled": false,
              "annotations": {},
              "hosts": [
                {
                  "host": "chart-example.local",
                  "paths": []
                }
              ],
              "tls": []
            },
            "resources": {},
            "nodeSelector": {},
            "tolerations": [],
            "affinity": {}
          }
        }
      ]
spec:
  apiservicedefinitions: {}
  customresourcedefinitions:
    owned:
    - kind: FfDL
      name: ffdls.mlx.com
      version: v1alpha1
      displayName: FfDL operator
      description: Fabric for Deep Learning
  description: |
    The FfDL Operator allows users to easily install [FfDL](https://github.com/IBM/FfDL/tree/helm-patch) on Kubernetes clusters. FfDL is an operating system fabric for Deep Learning. It is a collaboration platform for
    * Framework-independent training of Deep Learning models on distributed hardware

    * Open Deep Learning APIs

    * Running Deep Learning hosting in users private or public cloud
    
    To know more about the architectural details, please read the [design document](https://github.com/IBM/FfDL/blob/helm-patch/design/design_docs.md). If you are looking for demos, slides, collaterals, blogs, webinars and other materials related to FfDL, please find them [here](https://github.com/IBM/FfDL/tree/helm-patch/demos).
    
    ## Parameters
    
    * FFDL_NAMESPACE - namespace where to install FfDL

    * FFDL_STORAGECLASS - storage class for FfDL persistent volume claim

    ## Supported Deep Learning frameworks
    
    | Framework     | Versions      | Processing Unit |
    | ------------- | ------------- | --------------- |
    | [tensorflow](https://hub.docker.com/r/tensorflow/tensorflow/)    | 1.4.0, 1.4.0-py3, 1.5.0, 1.5.0-py3, 1.5.1, 1.5.1-py3, 1.6.0, 1.6.0-py3, 1.7.0, 1.7.0-py3, 1.8.0, 1.8.0-py3, 1.9.0, 1.9.0-py3, latest, latest-py3 | CPU |
    | [tensorflow](https://hub.docker.com/r/tensorflow/tensorflow/)    | 1.4.0-gpu, 1.4.0-gpu-py3, 1.5.0-gpu, 1.5.0-gpu-py3, 1.5.1-gpu, 1.5.1-gpu-py3, 1.6.0-gpu, 1.6.0-gpu-py3, 1.7.0-gpu, 1.7.0-gpu-py3, 1.8.0-gpu, 1.8.0-gpu-py3, 1.9.0-gpu, 1.9.0-gpu-py3, latest-gpu, latest-gpu-py3 | GPU |
    | [caffe](https://hub.docker.com/r/bvlc/caffe/)         | cpu, intel   | CPU |
    | [caffe](https://hub.docker.com/r/bvlc/caffe/)         | gpu           | GPU |
    | [pytorch](https://hub.docker.com/r/pytorch/pytorch/)       | v0.2, latest | CPU, GPU |
    | [caffe2](https://hub.docker.com/r/caffe2ai/caffe2/)        | c2v0.8.1.cpu.full.ubuntu14.04, c2v0.8.0.cpu.full.ubuntu16.04 | CPU |
    | [caffe2](https://hub.docker.com/r/caffe2ai/caffe2/)        | c2v0.8.1.cuda8.cudnn7.ubuntu16.04, latest | GPU |
    | [h2o3](https://hub.docker.com/r/opsh2oai/h2o3-ffdl/)    | latest | CPU |
    | [horovod](https://hub.docker.com/r/uber/horovod/)       | 0.13.10-tf1.9.0-torch0.4.0-py2.7, 0.13.10-tf1.9.0-torch0.4.0-py3.5 | CPU, GPU |
    
    More details please refer to [user guide](https://github.com/IBM/FfDL/blob/helm-patch/docs/user-guide.md).
  displayName: FfDL Operator
  icon:
  - base64data: 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
    mediatype: image/png
  install:
    spec:
      clusterPermissions:
      - rules:
        - apiGroups:
          - ""
          resources:
          - pods
          - services
          - endpoints
          - persistentvolumes
          - persistentvolumeclaims
          - events
          - configmaps
          - secrets
          - serviceaccounts
          verbs:
          - "*"
        - apiGroups:
          - ""
          resources:
          - namespaces
          verbs:
          - get
        - apiGroups:
          - apps
          resources:
          - deployments
          - daemonsets
          - replicasets
          - statefulsets
          verbs:
          - "*"
        - apiGroups:
          - extensions
          resources:
          - deployments
          - daemonsets
          verbs:
          - "*"
        - apiGroups:
          - rbac.authorization.k8s.io
          resources:
          - clusterrolebindings
          - clusterroles
          verbs:
          - "*"
        - apiGroups:
          - storage.k8s.io
          resources:
          - storageclasses
          verbs:
          - "*"
        - apiGroups:
          - monitoring.coreos.com
          resources:
          - servicemonitors
          verbs:
          - get
          - create
        - apiGroups:
          - apps
          resourceNames:
          - ffdl-operator
          resources:
          - deployments/finalizers
          verbs:
          - update
        - apiGroups:
          - mlx.com
          resources:
          - "*"
          verbs:
          - "*"
        serviceAccountName: ffdl-operator
      deployments:
      - name: ffdl-operator
        spec:
          replicas: 1
          selector:
            matchLabels:
              name: ffdl-operator
          strategy: {}
          template:
            metadata:
              labels:
                name: ffdl-operator
            spec:
              containers:
              - env:
                - name: WATCH_NAMESPACE
                  valueFrom:
                    fieldRef:
                      fieldPath: metadata.annotations["olm.targetNamespaces"]
                - name: POD_NAME
                  valueFrom:
                    fieldRef:
                      fieldPath: metadata.name
                - name: OPERATOR_NAME
                  value: ffdl-operator
                - name: FFDL_NAMESPACE
                  value: "default"
                - name: FFDL_STORAGECLASS
                  value: "ibmc-file-gold"
                - name: FFDL_LOCALSTORAGE
                  value: "false"
                image: ffdlops/ffdl:v0.0.1
                imagePullPolicy: Always
                name: ffdl-operator
                resources: {}
              serviceAccountName: ffdl-operator
    strategy: deployment
  installModes:
  - supported: true
    type: OwnNamespace
  - supported: true
    type: SingleNamespace
  - supported: false
    type: MultiNamespace
  - supported: true
    type: AllNamespaces
  maturity: alpha
  provider:
    name: IBM
  links:
  - name: FfDL
    url: https://github.com/IBM/FfDL
  - name: User Guide
    url: https://github.com/IBM/FfDL/blob/helm-patch/docs/user-guide.md
  keywords:
  - FfDL
  - Deep Learning
  version: 0.0.1
  maintainers:
  - name: IBM
    email: wzhuang@us.ibm.com`

export const JupyterData = 
`apiVersion: operators.coreos.com/v1alpha1
kind: ClusterServiceVersion
metadata:
  name: jupyterlab-operator.v0.0.1
  namespace: placeholder
  annotations:
    capabilities: Basic Install
    categories: "AI/Machine Learning"
    description: "Jupyter Lab"
    containerImage: docker.io/ffdlops/jupyterlab:v0.0.1
    support: TBD
    certified: "false"
    createdAt: 2019-04-29T08:00:00Z
    alm-examples: |-
      [{placeholder}]
spec:
  apiservicedefinitions: {}
  customresourcedefinitions:
    owned:
    - kind: Jupyterlab
      name: jupyterlabs.mlx.com
      version: v1alpha1
      displayName: Jupyterlab operator
      description: Operator for Jupyterhub and Enterprise Gateway
  description: |
    Next-generation web-based interface for Project Jupyter that enables users to work with documents and Jupyter notebooks, text editors, terminals and custom components side by side using tabs and splitters, in a flexible, integrated, and interactive manner.  It is similar to an IDE for developing comprehensive, interactive and exploratory notebook projects.
  displayName: Jupyterlab Operator
  icon:
  install:
    spec:
      clusterPermissions:
      - rules:
        - apiGroups:
          - ""
          resources:
          - pods
          - services
          - endpoints
          - persistentvolumes
          - persistentvolumeclaims
          - events
          - configmaps
          - secrets
          verbs:
          - '*'
        - apiGroups:
          - ""
          resources:
          - namespaces
          - serviceaccounts
          - pods/portforward
          verbs:
          - get
          - list
          - create
          - delete
        - apiGroups:
          - rbac.authorization.k8s.io
          resources:
          - clusterroles
          - clusterrolebindings
          - roles
          - rolebindings
          verbs:
          - get
          - list
          - create
          - delete
        - apiGroups:
          - apps
          resources:
          - deployments
          - daemonsets
          - replicasets
          - statefulsets
          verbs:
          - '*'
        - apiGroups:
          - monitoring.coreos.com
          resources:
          - servicemonitors
          verbs:
          - get
          - create
        - apiGroups:
          - apps
          resourceNames:
          - jupyterlab-operator
          resources:
          - deployments/finalizers
          verbs:
          - update
        - apiGroups:
          - mlx.com
          resources:
          - '*'
          verbs:
          - '*'
        - apiGroups:
          - extensions
          resources:
          - ingresses
          - podsecuritypolicies
          verbs:
          - '*'
        - apiGroups:
          - storage.k8s.io
          resources:
          - storageclasses
          - volumeattachments
          verbs:
          - '*'
        serviceAccountName: jupyterlab-operator
      deployments:
      - name: jupyterlab-operator
        spec:
          replicas: 1
          selector:
            matchLabels:
              name: jupyterlab-operator
          strategy: {}
          template:
            metadata:
              labels:
                name: jupyterlab-operator
            spec:
              containers:
              - command:
                - /usr/local/bin/ao-logs
                - /tmp/ansible-operator/runner
                - stdout
                image: ffdlops/jupyterlab:v0.0.1
                imagePullPolicy: Always
                name: ansible
                resources: {}
                volumeMounts:
                - mountPath: /tmp/ansible-operator/runner
                  name: runner
                  readOnly: true
              - env:
                - name: WATCH_NAMESPACE
                  valueFrom:
                    fieldRef:
                      fieldPath: metadata.namespace
                - name: POD_NAME
                  valueFrom:
                    fieldRef:
                      fieldPath: metadata.name
                - name: OPERATOR_NAME
                  value: jupyterlab-operator
                - name: ANSIBLE_INVENTORY
                  value: /opt/ansible/inventory
                image: ffdlops/jupyterlab:v0.0.1
                imagePullPolicy: Always
                name: operator
                resources: {}
                volumeMounts:
                - mountPath: /tmp/ansible-operator/runner
                  name: runner
              serviceAccountName: jupyterlab-operator
              volumes:
              - emptyDir: {}
                name: runner
    strategy: deployment
  installModes:
  - supported: true
    type: OwnNamespace
  - supported: true
    type: SingleNamespace
  - supported: false
    type: MultiNamespace
  - supported: true
    type: AllNamespaces
  maturity: alpha
  provider:
    name: TBD
  links:
  - name: JupyterHub
    url: placeholder url
  - name: Enterprise Gateway
    url: placeholder url
  keywords:
  - JupyterHub
  - Enterprise Gateway
  version: 0.0.1
  maintainers:
  - name: TBD
    email: placeholder email`

export const PipelinesData = 
`apiVersion: operators.coreos.com/v1alpha1
kind: ClusterServiceVersion
metadata:
  name: pipelines-operator.v0.0.1
  namespace: placeholder
  annotations:
    capabilities: Basic Install
    categories: "AI/Machine Learning"
    description: "Kubeflow Pipelines"
    containerImage: docker.io/ffdlops/pipelines:v0.0.1
    support: TBD
    certified: "false"
    createdAt: 2019-04-29T08:00:00Z
    alm-examples: |-
      [{placeholder}]
spec:
  apiservicedefinitions: {}
  customresourcedefinitions:
    owned:
    - kind: Pipelines
      name: pipelines.mlx.com
      version: v1alpha1
      displayName: Pipelines Operator
      description: Operator for deploying minimal Kubeflow pipelines
  description: |
    A platform to build and deploy portable, scalable machine learning workflows based on docker containers. It consists of a user interface for managing and tracking experiments, jobs and runs, an engine for scheduling ML workflows, an SDK for defining and manipulating pipelines and components and notebooks for interacting with system using the SDK. It is the executing engine for MLX pipelines and components. 
  displayName: Pipelines Operator
  icon:
  install:
    spec:
      clusterPermissions:
      - rules:
        - apiGroups:
          - ""
          resources:
          - pods
          - services
          - endpoints
          - persistentvolumes
          - persistentvolumeclaims
          - events
          - configmaps
          - secrets
          verbs:
          - '*'
        - apiGroups:
          - ""
          resources:
          - namespaces
          - serviceaccounts
          - pods/portforward
          verbs:
          - '*'
        - apiGroups:
          - rbac.authorization.k8s.io
          resources:
          - clusterroles
          - clusterrolebindings
          - roles
          - rolebindings
          verbs:
          - get
          - list
          - create
          - delete
        - apiGroups:
          - apps
          resources:
          - deployments
          - daemonsets
          - replicasets
          - statefulsets
          verbs:
          - '*'
        - apiGroups:
          - monitoring.coreos.com
          resources:
          - servicemonitors
          verbs:
          - get
          - create
        - apiGroups:
          - apps
          resourceNames:
          - pipelines-operator
          resources:
          - deployments/finalizers
          verbs:
          - update
        - apiGroups:
          - extensions
          resources:
          - ingresses
          - podsecuritypolicies
          - deployments
          verbs:
          - '*'
        - apiGroups:
          - mlx.com
          resources:
          - '*'
          verbs:
          - '*'
        - apiGroups:
          - app.k8s.io
          resources:
          - applications
          verbs:
          - '*'
        serviceAccountName: pipelines-operator
      deployments:
      - name: pipelines-operator
        spec:
          replicas: 1
          selector:
            matchLabels:
              name: pipelines-operator
          strategy: {}
          template:
            metadata:
              labels:
                name: pipelines-operator
            spec:
              containers:
              - command:
                - /usr/local/bin/ao-logs
                - /tmp/ansible-operator/runner
                - stdout
                image: ffdlops/kfp:v0.0.1
                imagePullPolicy: Always
                name: ansible
                resources: {}
                volumeMounts:
                - mountPath: /tmp/ansible-operator/runner
                  name: runner
                  readOnly: true
              - env:
                - name: WATCH_NAMESPACE
                  valueFrom:
                    fieldRef:
                      fieldPath: metadata.namespace
                - name: POD_NAME
                  valueFrom:
                    fieldRef:
                      fieldPath: metadata.name
                - name: OPERATOR_NAME
                  value: pipelines-operator
                image: ffdlops/kfp:v0.0.1
                imagePullPolicy: Always
                name: operator
                resources: {}
                volumeMounts:
                - mountPath: /tmp/ansible-operator/runner
                  name: runner
              serviceAccountName: pipelines-operator
              volumes:
              - emptyDir: {}
                name: runner
    strategy: deployment
  installModes:
  - supported: true
    type: OwnNamespace
  - supported: true
    type: SingleNamespace
  - supported: false
    type: MultiNamespace
  - supported: true
    type: AllNamespaces
  maturity: alpha
  provider:
    name: TBD
  links:
  - name: Kubeflow Pipelines
    url: github.com/kubeflow/pipelines
  keywords:
  - Pipelines
  - Kubeflow
  version: 0.0.1
  maintainers:
  - name: TBD
    email: placeholder email`

export const IstioData = 
`#! validate-crd: deploy/chart/templates/0000_30_02-clusterserviceversion.crd.yaml
#! parse-kind: ClusterServiceVersion
apiVersion: istio.banzaicloud.io/v1beta1
kind: ClusterServiceVersion
metadata:
  name: istio-operator.0.1.6
  namespace: placeholder
  annotations:
    capabilities: Full Lifecycle
    categories: "Monitoring, Logging & Tracing, Security"
    certified: "false"
    description: Installs and maintain Istio service mesh
    containerImage: banzaicloud/istio-operator:0.1.6
    repository: https://github.com/banzaicloud/istio-operator/tree/release-1.1
    createdAt: "2019-04-01T08:00:00Z"
    support: Banzai Cloud
    alm-examples: |
      [
        {
            "apiVersion": "istio.banzaicloud.io/v1beta1",
            "kind": "Istio",
            "metadata": {
                "name": "istio-sample"
            },
            "spec": {
                "autoInjectionNamespaces": [
                    "default"
                ],
                "citadel": {
                    "image": "docker.io/istio/citadel:1.1.2",
                    "replicaCount": 1
                },
                "defaultPodDisruptionBudget": {
                    "enabled": true
                },
                "galley": {
                    "image": "docker.io/istio/galley:1.1.2",
                    "replicaCount": 1
                },
                "gateways": {
                    "egress": {
                        "maxReplicas": 5,
                        "minReplicas": 1,
                        "replicaCount": 1,
                        "sds": {
                            "image": "node-agent-k8s"
                        }
                    },
                    "ingress": {
                        "maxReplicas": 5,
                        "minReplicas": 1,
                        "replicaCount": 1,
                        "sds": {
                            "image": "node-agent-k8s"
                        }
                    },
                    "k8singress": {}
                },
                "imageHub": "docker.io/istio",
                "imageTag": "1.1.0",
                "includeIPRanges": "*",
                "mixer": {
                    "image": "docker.io/istio/mixer:1.1.2",
                    "maxReplicas": 5,
                    "minReplicas": 1,
                    "replicaCount": 1
                },
                "mtls": false,
                "nodeAgent": {
                    "image": "docker.io/istio/node-agent-k8s:1.1.2"
                },
                "outboundTrafficPolicy": {
                    "mode": "ALLOW_ANY"
                },
                "pilot": {
                    "image": "docker.io/istio/pilot:1.1.2",
                    "maxReplicas": 5,
                    "minReplicas": 1,
                    "replicaCount": 1,
                    "traceSampling": 1
                },
                "proxy": {
                    "image": "docker.io/istio/proxyv2:1.1.2"
                },
                "proxyInit": {
                    "image": "docker.io/istio/proxy_init:1.1.2"
                },
                "sds": {},
                "sidecarInjector": {
                    "image": "docker.io/istio/sidecar_injector:1.1.2",
                    "replicaCount": 1,
                    "rewriteAppHTTPProbe": true
                },
                "tracing": {
                    "zipkin": {
                        "address": "zipkin.istio-system:9411"
                    }
                },
                "version": "1.1.2"
            }
        },
        {
            "apiVersion": "istio.banzaicloud.io/v1beta1",
            "kind": "RemoteIstio",
            "metadata": {
                "name": "remoteistio-sample"
            },
            "spec": {
                "autoInjectionNamespaces": [
                    "default"
                ],
                "citadel": {
                    "enabled": true,
                    "replicaCount": 1
                },
                "enabledServices": [
                    {
                        "labelSelector": "istio=pilot",
                        "name": "istio-pilot"
                    },
                    {
                        "labelSelector": "istio-mixer-type=policy",
                        "name": "istio-policy"
                    },
                    {
                        "labelSelector": "statsd-prom-bridge",
                        "name": "istio-statsd"
                    },
                    {
                        "labelSelector": "istio-mixer-type=telemetry",
                        "name": "istio-telemetry"
                    },
                    {
                        "labelSelector": "app=jaeger",
                        "name": "zipkin"
                    }
                ],
                "includeIPRanges": "*",
                "proxy": {},
                "proxyInit": {},
                "sidecarInjector": {
                    "enabled": true,
                    "initCNIConfiguration": {},
                    "replicaCount": 1
                }
            }
        }
      ]
spec:
  displayName: Istio
  description: |
    Istio-operator is a Kubernetes operator to deploy and manage [Istio](https://istio.io/) resources for a Kubernetes cluster.

    ## Overview

    [Istio](https://istio.io/) is an open platform to connect, manage, and secure microservices and it is emerging as the **standard** for building service meshes on Kubernetes. It is built out on multiple components and a rather complex deployment scheme (around 14 Helm subcharts and 50+ CRDs). Installing, upgrading and operating these components requires deep understanding of Istio and Helm (the standard/supported way of deploying [Istio](https://istio.io/)).

    The goal of the **Istio-operator** is to automate and simplify these and enable popular service mesh use cases (multi cluster federation, canary releases, resource reconciliation, etc) by introducing easy higher level abstractions.
  keywords: ['istio', 'multi cluster', 'federation', 'service mesh', 'banzaicloud', 'open source']
  version: 0.1.6
  maturity: beta
  maintainers:
  - name: Banzai Cloud
    email: info@banzaicloud.com
  provider:
    name: Banzai Cloud
  labels:
    alm-owner-istio: istio-operator
    operated-by: istio-operator
  selector:
    matchLabels:
      alm-owner-istio: istio-operator
      operated-by: istio-operator
  links:
  - name: Blog
    url: https://banzaicloud.com/tags/istio
  - name: Documentation
    url: https://github.com/banzaicloud/istio-operator/blob/release-1.1/README.md
  - name: Istio Operator Source Code
    url: https://github.com/banzaicloud/istio-operator/tree/release-1.1

  icon:
  - base64data: PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz4KPHN2ZyB2ZXJzaW9uPSIxLjEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld0JveD0iMCAwIDMyMCAzMjAiPgogIDxnIGlkPSJsb2dvIiBmaWxsPSIjZmZmIj4KICAgIDxyZWN0IGlkPSJiYWNrZ3JvdW5kIiBmaWxsPSIjNDY2QkIwIiB3aWR0aD0iMzIwIiBoZWlnaHQ9IjMyMCIgLz4KICAgIDxwb2x5Z29uIGlkPSJodWxsIiBwb2ludHM9IjgwIDI1MCAyNDAgMjUwIDE0MCAyODAgODAgMjUwIi8+CiAgICA8cG9seWdvbiBpZD0ibWFpbnNhaWwiIHBvaW50cz0iODAgMjQwIDE0MCAyMzAgMTQwIDEyMCA4MCAyNDAiLz4KICAgIDxwb2x5Z29uIGlkPSJoZWFkc2FpbCIgcG9pbnRzPSIxNTAgMjMwIDI0MCAyNDAgMTUwIDQwIDE1MCAyMzAiLz4KICA8L2c+Cjwvc3ZnPgo=
    mediatype: image/svg+xml
  installModes:
  - type: OwnNamespace
    supported: true
  - type: SingleNamespace
    supported: false
  - type: MultiNamespace
    supported: false
  - type: AllNamespaces
    supported: true
  install:
    strategy: deployment
    spec:
      clusterPermissions:
      - serviceAccountName: istio-operator
        rules:
        - apiGroups:
          - apps
          resources:
          - pods
          verbs:
          - get
          - list
          - watch
        - apiGroups:
          - apps
          resources:
          - pods/status
          verbs:
          - get
        - apiGroups:
          - ""
          resources:
          - nodes
          - services
          - endpoints
          - pods
          - replicationcontrollers
          - services
          - endpoints
          - pods
          verbs:
          - get
          - list
          - watch
        - apiGroups:
          - ""
          resources:
          - serviceaccounts
          - configmaps
          verbs:
          - get
          - list
          - watch
          - create
          - update
          - patch
          - delete
        - apiGroups:
          - ""
          resources:
          - namespaces
          verbs:
          - get
          - list
          - watch
          - update
          - patch
        - apiGroups:
          - apps
          resources:
          - replicasets
          verbs:
          - get
          - list
          - watch
        - apiGroups:
          - apps
          resources:
          - deployments
          - daemonsets
          verbs:
          - get
          - list
          - watch
          - create
          - update
          - patch
          - delete
        - apiGroups:
          - apps
          resources:
          - deployments/status
          verbs:
          - get
          - update
          - patch
        - apiGroups:
          - extensions
          resources:
          - ingresses
          - ingresses/status
          verbs:
          - '*'
        - apiGroups:
          - extensions
          resources:
          - deployments
          verbs:
          - get
        - apiGroups:
          - extensions
          resources:
          - deployments/finalizers
          verbs:
          - update
        - apiGroups:
          - extensions
          resources:
          - replicasets
          verbs:
          - get
          - list
          - watch
        - apiGroups:
          - policy
          resources:
          - poddisruptionbudgets
          verbs:
          - get
          - list
          - watch
          - create
          - update
          - patch
          - delete
        - apiGroups:
          - autoscaling
          resources:
          - horizontalpodautoscalers
          verbs:
          - get
          - list
          - watch
          - create
          - update
          - patch
          - delete
        - apiGroups:
          - apiextensions.k8s.io
          resources:
          - customresourcedefinitions
          verbs:
          - '*'
        - apiGroups:
          - istio.banzaicloud.io
          resources:
          - istios
          verbs:
          - get
          - list
          - watch
          - create
          - update
          - patch
          - delete
        - apiGroups:
          - istio.banzaicloud.io
          resources:
          - istios/status
          verbs:
          - get
          - update
          - patch
        - apiGroups:
          - authentication.istio.io
          - cloud.istio.io
          - config.istio.io
          - istio.istio.io
          - networking.istio.io
          - rbac.istio.io
          - scalingpolicy.istio.io
          resources:
          - '*'
          verbs:
          - '*'
        - apiGroups:
          - apps
          resources:
          - deployments
          verbs:
          - get
          - list
          - watch
          - create
          - update
          - patch
          - delete
        - apiGroups:
          - apps
          resources:
          - deployments/status
          verbs:
          - get
          - update
          - patch
        - apiGroups:
          - istio.banzaicloud.io
          resources:
          - remoteistios
          verbs:
          - get
          - list
          - watch
          - create
          - update
          - patch
          - delete
        - apiGroups:
          - istio.banzaicloud.io
          resources:
          - remoteistios/status
          verbs:
          - get
          - update
          - patch
        - apiGroups:
          - admissionregistration.k8s.io
          resources:
          - validatingwebhookconfigurations
          verbs:
          - get
          - list
          - watch
          - create
          - update
          - patch
          - delete
        - apiGroups:
          - istio.banzaicloud.io
          resources:
          - istios
          verbs:
          - get
          - list
          - watch
        - apiGroups:
          - rbac.authorization.k8s.io
          resources:
          - clusterroles
          - clusterrolebindings
          - roles
          - rolebindings
          - ""
          verbs:
          - get
          - list
          - watch
          - create
          - update
          - patch
          - delete
        - apiGroups:
          - authentication.k8s.io
          resources:
          - tokenreviews
          verbs:
          - create
        - apiGroups:
          - admissionregistration.k8s.io
          resources:
          - mutatingwebhookconfigurations
          - validatingwebhookconfigurations
          verbs:
          - '*'
        - apiGroups:
          - ""
          resources:
          - secrets
          verbs:
          - get
          - list
          - watch
          - create
          - update
          - patch
          - delete
        - apiGroups:
          - ""
          resources:
          - services
          verbs:
          - get
          - list
          - watch
          - create
          - update
          - patch
          - delete
      deployments:
      - name: istio-operator
        spec:
          replicas: 1
          selector:
            matchLabels:
              k8s-app: istio-operator
              control-plane: controller-manager
              controller-tools.k8s.io: "1.0"
          template:
            metadata:
              annotations:
                prometheus.io/scrape: "true"
                prometheus.io/port: "8080"
              labels:
                k8s-app: istio-operator
                control-plane: controller-manager
                controller-tools.k8s.io: "1.0"
            spec:
              serviceAccountName: istio-operator
              containers:
              - name: istio-operator
                command:
                - /manager
                args:
                - --metrics-addr=:8080
                - --watch-created-resources-events=true
                image: banzaicloud/istio-operator:0.1.6
                imagePullPolicy: Always
                resources:
                  limits:
                    cpu: 200m
                    memory: 256Mi
                  requests:
                    cpu: 100m
                    memory: 128Mi
                env:
                - name: POD_NAMESPACE
                  valueFrom:
                    fieldRef:
                      fieldPath: metadata.namespace
                - name: WATCH_NAMESPACE
                  valueFrom:
                    fieldRef:
                      fieldPath: metadata.annotations['olm.targetNamespaces']
                ports:
                - containerPort: 443
                  name: webhook-server
                  protocol: TCP
                - containerPort: 8080
                  name: metrics
                  protocol: TCP
              terminationGracePeriodSeconds: 60
  customresourcedefinitions:
    owned:
    - name: istios.istio.banzaicloud.io
      version: v1beta1
      kind: Istio
      displayName: Istio service mesh
      description: Represents an Istio service mesh
    - name: remoteistios.istio.banzaicloud.io
      version: v1beta1
      kind: RemoteIstio
      displayName: Remote member cluster
      description: Represents a Remote Cluster of an Istio service mesh`
