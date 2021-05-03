// Copyright 2021 IBM Corporation
// 
// Licensed under the Apache License, Version 2.0 (the "License"); 
// you may not use this file except in compliance with the License. 
// You may obtain a copy of the License at 
// 
//     http://www.apache.org/licenses/LICENSE-2.0 
// 
// Unless required by applicable law or agreed to in writing, software 
// distributed under the License is distributed on an "AS IS" BASIS, 
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
// See the License for the specific language governing permissions and 
// limitations under the License. 
const PIPELINE_DATA = [
  {
    'id':'0',
    'category':'Open Source',
    'description':'This pipeline trains 2 models, does fairness and robustness checking, then does canary test with Knative for deployment.',
    'link': 'http://aiops-demo.info/pipeline/#/pipelines/details/b8a71b25-0ec8-4037-b49f-94c37acf50e1',
    'name':'Train with FfDL and canary testing with Knative',
  },
  {
    'id': '1',
    'category':'Open Source',
    'description':'A simple IBM OSS pipeline demonstrates how to train a model using Fabric for Deep Learning and then deploy it with Seldon.',
    'link':'http://aiops-demo.info/pipeline/#/pipelines/details/81dfd4bf-c4b1-4371-bca0-222aae8fbe53',
    'name':'Train and deploy with FfDL and Seldon (OSS)',
  },
  { 
    'id':'2',
    'category':'IBM Watson',
    'description':'A sample pipeline for training, storing and deploying a Tensorflow model with MNIST handwriting recognition on IBM Watson Machine Learning service.',
    'link':'http://aiops-demo.info/pipeline/#/pipelines/details/030e3b3a-705f-45c1-9608-2180ec93a3a1',
    'name':'Train and deploy with Watson Machine Learning',
  },
  {
    'id':'3',
    'category':'Open Source',
    'description':'IBM AI OpenScale to monitor and analyze ML models.',
    'link':'http://aiops-demo.info/pipeline/#/pipelines/details/e2820339-ee7b-451b-b9ab-b0bdf616d1f5',
    'name':'Model analysis and operations using AI OpenScale',
  },
  {
    'id':'4',
    'category':'IBM Watson',
    'description':'This AI pipeline uses FfDLto train a model, does fairness checking and robustness checking. For successful checking results, it does the model deployment with A/B testing.',
    'link':'http://aiops-demo.info/pipeline/#/pipelines/details/f246bd8a-832e-4560-a8db-3cbee851c3fd',
    'name':'End-to-end pipeline with fairness and robustness test.',
  },
  {
    'id':'5',
    'category':'IBM Watson',
    'description':'Deploy a container to a Kuberentes platform with its own service.',
    'link': 'http://aiops-demo.info/pipeline/#/pipelines/details/7bf6eb57-f41b-4703-a769-d0c97f7e11bf',
    'name':'Kubernetes model deployment',
  },
  {
    'id': '6',
    'category':'Open Source',
    'description':'Deploy a container to a Knative platform with traffic splitting.',
    'link':'http://aiops-demo.info/pipeline/#/pipelines/details/f64b0431-877d-42e3-84e2-8ca12f4ba53e',
    'name':'Knative model deployment',
  },
  { 
    'id':'7',
    'category':'IBM Watson',
    'description':'A pipeline shows how to use dsl.Condition.',
    'link':'http://aiops-demo.info/pipeline/#/pipelines/details/d3b884ac-9645-4a65-a0cc-5539f17a56da',
    'name':'[Sample] Basic - Condition',
  },
  {
    'id':'8',
    'category':'IBM Watson',
    'description':'A pipeline that downloads two messages in parallel and print the concatenated result.',
    'link':'http://aiops-demo.info/pipeline/#/pipelines/details/00680ba3-9cf1-4f1f-a61b-88e1ae2a0531',
    'name':'[Sample] Basic - Parallel Join',
  },
  {
    'id':'9',
    'category':'Open Source',
    'description':'A trainer that does end-to-end distributed training for XGBoost models.',
    'link':'http://aiops-demo.info/pipeline/#/pipelines/details/592b9d93-587f-4c1a-914c-03a66db296e2',
    'name':'[Sample] ML - XGBoost - Training with Confusion Matrix',
  }
];

export default PIPELINE_DATA;
