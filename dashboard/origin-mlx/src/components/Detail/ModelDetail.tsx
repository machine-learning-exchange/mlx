/* 
*  Copyright 2021 IBM Corporation
* 
*  Licensed under the Apache License, Version 2.0 (the "License"); 
*  you may not use this file except in compliance with the License. 
*  You may obtain a copy of the License at 
* 
*      http://www.apache.org/licenses/LICENSE-2.0 
* 
*  Unless required by applicable law or agreed to in writing, software 
*  distributed under the License is distributed on an "AS IS" BASIS, 
*  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
*  See the License for the specific language governing permissions and 
*  limitations under the License. 
*/ 
import * as React from 'react';
import StoreContext from '../../lib/stores/context'
import { capitalize, getUserInfo, hasRole } from '../../lib/util'

import Grid from '@material-ui/core/Grid';
import LoadingMessage from '../LoadingMessage';
import ModelRunForm from '../RunView/ModelRunView';
import SourceCodeDisplay from '../SourceCodeDisplay';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import MetadataView from '../MetadataView';

const isAdmin = hasRole(getUserInfo(), 'admin');

export interface ModelDetailProps {
  setRunLink?: Function
  name?: string
  asset?: any
}

export interface ModelDetailState {
  leftTab: string
  rightTab: string
  codeTab: string
  model: {
    template: any,
    yaml: string,
    [props: string]: any
  }
}

export default class ModelDetail extends React.Component<ModelDetailProps, ModelDetailState> {
  static contextType = StoreContext

  constructor(props: any) {
    super(props);
    this.state = {
      rightTab: 'source',
      leftTab: 'detail',
      codeTab: '',
      model: props.asset,
    };
  }

  async componentDidMount() {
    const { store } = this.context
    const { api } = store.settings.endpoints
    const API = api.value || api.default

    const model = this.state.model

    const codeRes = await fetch(`${API}/apis/v1alpha1/models/${model.id}/generate_code`)

    this.setState({
      model: { ...model, code: (await codeRes.json()).scripts, }
    })
  }

  getCodeType = (tab:string) => {
    switch (tab) {
      case 'serve':
        return this.state.model.servable_tested_platforms
      case 'train':
        return this.state.model.trainable_tested_platforms
      default:
        return ['']
    }
  }

  getCode = (platform: string) =>
    this.state.model.code
      .find(({ execution_platform }: any) =>
        execution_platform === platform).script_code

  public render() {
    const { store } = this.context
    const { api, kfp } = store.settings.endpoints
    const API = api.value || api.default
    const KFP = kfp.value || kfp.default
    const { execute } = store.settings.capabilities
    const canRun = execute.value !== null ? execute.value : execute.default
    const setRunLink = this.props.setRunLink

    const model = this.state.model

    const showCode = this.state.rightTab === 'serve' || this.state.rightTab === 'train'
  
    return (
      <Grid
        container
        spacing={ 0 } 
        justify="center">
        <Grid 
          className="left-wrapper"
          item xs={ 6 }>

          <div className="tab-nav">
            <Tabs 
              variant="fullWidth"
              className="comp-tabs" 
              value={ this.state.leftTab }
              onChange={(_, value: string) => this.setState({ leftTab: value })}>
              <Tab 
                className="comp-tab"
                value="detail" 
                label="Details" 
              />
              {canRun && isAdmin &&
                <Tab 
                  className="comp-tab"
                  value="runCreation" 
                  label="Launch" 
                />
              }
            </Tabs>
          </div>
          {this.state.leftTab === 'detail' &&
            <MetadataView content={{
              about: [
                { name: "model identifier", data: model.template.model_identifier },
                { name: "domain", data: model.template.domain },
                { name: "description", data: model.template.description },
              ],
              'Usage Info': [
                { 
                  name: "framework name",
                  data: capitalize(model.template.framework.name),
                  thirdColData: model.template.framework.version ? ` v` + model.template.framework.version: ''
                },
                model.isTrainable && { 
                  name: "runtime",
                  data: capitalize(model.template.framework.runtimes.name),
                  thirdColData: model.template.framework.runtimes ? ` v` + model.template.framework.runtimes.version: ''
                },
                { name: "license", data: model.template.license },
                { name: "website", data: model.template.website, itemClass: "model-link" },
              ],
              'Serving Details': model.isServable && [
                { 
                  name: "tested platforms",
                  data: model.template.serving.tested_platforms.map((name:string)=>name).join(`, `)
                },
                { 
                  name: "container image",
                  data: String(model.template.serving.serving_container_image.container_image_url)
                },
              ],
              'Training Details': model.isTrainable && [
                { 
                  name: "tested platforms",
                  data: model.template.training.tested_platforms.map((name:string)=>name).join(`, `)
                },
                model.template.training.training_container_image && { 
                  name: "container image",
                  data: model.template.training.training_container_image ? model.template.training.training_container_image.container_image_url : ``
                },
                { 
                  name: "execution command",
                  data: model.template.training.execution.command
                },
              ]
            }}/>
          }
          {this.state.leftTab === 'runCreation' &&
            <ModelRunForm 
              servableCredentialsRequired={model.servable_credentials_required || false} 
              trainableCredentialsRequired={model.trainable_credentials_required || false} 
              trainingPlatforms={model.trainable_tested_platforms || []}
              servingPlatforms={model.servable_tested_platforms || []}
              inputParameters={model.template.serve ? model.template.serve.input_params : []}
              urlParameters={model.url_parameters || {}}
              id={model.id}
              KFP={KFP}
              API={API}
              setRunLink={setRunLink}
            />}
        </Grid>
        <Grid 
          className="right-wrapper"
          item xs={ 6 }>
          <div className="tab-nav">
            <Tabs 
              variant="fullWidth"
              className="comp-tabs" 
              value={ this.state.rightTab }
              onChange={(_, value: string) => this.setState({
                rightTab: value,
                codeTab: this.getCodeType(value)[0]
              })}>
              <Tab 
                className="comp-tab"
                value="source" 
                label="YAML Definition"
              />
              {model.servable &&
                <Tab 
                  className="comp-tab"
                  value="serve" 
                  label="Sample Serving Code"
                />
              }
              {model.trainable &&
                <Tab 
                  className="comp-tab"
                  value="train" 
                  label="Sample Training Code"
                />
              }
            </Tabs>
          </div>

          {/* BEGIN: second tab row */}
          {showCode &&
            <div className="tab-nav second-row">
              <Tabs
                variant="fullWidth"
                className="comp-tabs second-row" 
                value={this.state.codeTab || this.setState({
                  codeTab: this.getCodeType(this.state.rightTab)[0]
                })}
                onChange={(_, value: string) => this.setState({ codeTab: value })}
              >
                {this.getCodeType(this.state.rightTab).filter((platform : string) => platform !== "knative").map((platform: string) =>
                  <Tab 
                    key={platform}
                    className="comp-tab"
                    value={platform}
                    label={platform}
                  />
                )}
              </Tabs>
            </div>
          }
          {/* END: second tab row */}

          {this.state.rightTab === "source" &&
            <SourceCodeDisplay 
              isYAML={ true }
              code={model.yaml}
            />
          }
          {this.state.rightTab !== 'source' && (!model.code
              ? <LoadingMessage message="Loading Model sample code..." />
              : <SourceCodeDisplay 
                  isYAML={false}
                  code={this.getCode(this.state.codeTab)}
                />
          )}
        </Grid>
      </Grid>
    )
  }
}
