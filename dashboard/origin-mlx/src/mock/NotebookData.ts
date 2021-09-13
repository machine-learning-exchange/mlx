// Copyright 2021 IBM Corporation
// 
// SPDX-License-Identifier: Apache-2.0
export const OPENAI_NB =
`name: 'Notebook'
description: 'Sample notebook'
metadata:
  annotations:
    platform: 'OpenSource'
implementation:
  github:
    source: 'https://github.com/tomcli/notebook-folder/blob/master/simple-ibm-oss.ipynb'`

export const OPENAI_NB_JSON = [
  {
    name: 'Notebook',
    description: 'Sample notebook',
    metadata: {
      annotations: {
        platform: 'OpenSource'
      }
    },
    implementation: {
      github: {
        source: 'https://github.com/tomcli/notebook-folder/blob/master/simple-ibm-oss.ipynb'
      }
    }
  },
]

export const NOTEBOOK_LIST = 
`name: 'AIF360 Gender Classification'
description: 'Notebook to train AIF360 Gender Classification with reweighing'
metadata:
  annotations:
    platform: 'OpenSource'
implementation:
  github:
    source: 'https://github.com/IBM/AIF360/blob/master/examples/tutorial_gender_classification.ipynb'
---
name: 'ART detector model'
description: 'Notebook to train ART detector model to dector possible adversarial attack'
metadata:
  annotations:
    platform: 'OpenSource'
implementation:
  github:
    source: 'https://github.com/IBM/adversarial-robustness-toolbox/blob/master/notebooks/detector-for-CIFAR10.ipynb'
---
name: 'ART poisoning attack'
description: 'Use Notebook to leverage ART for poisoning training data and learn how to defends it'
metadata:
  annotations:
    platform: 'OpenSource'
implementation:
  github:
    source: 'https://github.com/IBM/adversarial-robustness-toolbox/blob/master/notebooks/mnist_poisoning_demo.ipynb'
---
name: 'End-to-end with fairness and robustness test'
description: 'This notebook uses FfDL to train a model, does fairness checking and robustness checking. For successful checking results, it does the model deployment with A/B testing. Otherwise, it will restart the notebook pipeline with different parameters.'
metadata:
  annotations:
    platform: 'OpenSource'
implementation:
  github:
    source: 'https://github.com/machine-learning-exchange/katalog/blob/main/notebook-samples/e2e-pipeline/e2e-pipeline.ipynb'
---
name: 'Watson OpenScale'
description: 'A notebook showcases how to train custom Spark model on the Cloud and use IBM WatsonOpenScale to monitor and analyze ML model'
metadata:
  annotations:
    platform: 'Watson OpenScale'
implementation:
  github:
    source: 'https://github.com/machine-learning-exchange/katalog/blob/main/notebook-samples/watson-openscale/watson-openscale.ipynb'
---
name: 'Watson OpenScale walk through'
description: 'End to End Watson OpenScale walk through'
metadata:
  annotations:
    platform: 'Watson OpenScale'
implementation:
  github:
    source: 'https://github.com/machine-learning-exchange/katalog/blob/main/notebook-samples/watson-openscale/german_credit_train_and_config.ipynb'
---
name: 'Train and deploy with Watson Machine Learning'
description: 'Notebook for Training and deploying with Watson Machine Learning.'
metadata:
  annotations:
    platform: 'Watson Machine Learning'
implementation:
  github:
    source: 'https://github.com/machine-learning-exchange/katalog/blob/main/notebook-samples/Watson-ML-pipeline/watson-ml-pipeline.ipynb'`
