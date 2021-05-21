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
import { getUserInfo, hasRole } from '../../lib/util';

import Grid from '@material-ui/core/Grid'
import SourceCodeDisplay from '../SourceCodeDisplay'
import RunView from '../RunView'
import LoadingMessage from '../LoadingMessage'
import MetadataView from '../MetadataView'
import Tabs from '@material-ui/core/Tabs'
import Tab from '@material-ui/core/Tab'
import Typography from '@material-ui/core/Typography'

const isAdmin = hasRole(getUserInfo(), 'admin');

export interface ComponentDetailProps {
  setRunLink?: Function
  id?: string
  asset?: any
}

export interface ComponentDetailState {
  component: {
    template: any,
    yaml: string,
    [props: string]: any
  }
  leftTab: string
  rightTab: string
}

export default class ComponentDetail extends React.Component<ComponentDetailProps, ComponentDetailState> {
  static contextType = StoreContext

  constructor(props: any) {
    super(props);
    this.state = {
      rightTab: 'source',
      leftTab: 'detail',
      component: props.asset,
    }
  }

  async componentDidMount() {
    const { store } = this.context
    const { api } = store.settings.endpoints
    const API = api.value || api.default

    const component = this.state.component
    const codeRes = await fetch(`${API}/apis/v1alpha1/components/${component.id}/generate_code`);

    this.setState({
      component: {
        ...component,
        code: (await codeRes.json()).script
      }
    })
  }
  
  public render() {
    const { store } = this.context
    const { execute } = store.settings.capabilities
    const canRun = execute.value !== null ? execute.value : execute.default
    const setRunLink = this.props.setRunLink

    const component = this.state.component

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
              onChange={(_, leftTab: string) => this.setState({ leftTab })}>
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
            <MetadataView
              content={{
                inputs: component.template.inputs,
                outputs: component.template.outputs,
                arguments: [
                  <span className="args" style={{
                    maxWidth: '90% !important'
                  }}>
                    <Typography 
                      className="arg-heavy"
                      variant="h6" 
                      inline>
                      { (component.template.implementation.container.command || 'python') + ` ` }
                    </Typography>
                    {component.template.implementation.container.args.map((arg: any, i: number) => 
                      (typeof arg === 'string')
                        ? <Typography 
                            key={arg + i}
                            className="arg-heavy"
                            variant="h6" 
                            inline>
                            {arg + ' '}
                          </Typography>
                        : <i key={arg.inputValue + i}>
                            <Typography 
                              className="arg-light"
                              variant="subheading" 
                              inline>
                              {(arg.inputValue || arg.outputPath) + ' '}
                            </Typography>
                          </i>
                    )}
                    <div style={{ height: '2rem' }} />
                  </span>,
                  { name: 'command', description: component.template.implementation.container.command },
                  { name: 'image', description: component.template.implementation.container.image }
                ]
              }}
            />
          }
          { this.state.leftTab === 'runCreation' &&
            <RunView type={'components'} asset={component} setRunLink={setRunLink}/> 
          }
        </Grid>
        <Grid 
          className="right-wrapper"
          item xs={ 6 }>
          <div className="tab-nav">
          <Tabs 
            variant="fullWidth"
            className="comp-tabs" 
            value={this.state.rightTab}
            onChange={(_, rightTab: string) => this.setState({ rightTab })}>
            <Tab 
              className="comp-tab"
              value="source" 
              label="YAML Definition"
            />
            <Tab 
              className="comp-tab"
              value="sample" 
              label="Sample Pipeline Code"
            />
          </Tabs>
          </div>
          {this.state.rightTab === "source" &&
            <SourceCodeDisplay 
              isYAML={ true }
              code={component.yaml}
            />}
          {this.state.rightTab === 'sample' && (!component.code
            ? <LoadingMessage message="Loading component code..." />
            : <SourceCodeDisplay 
                isYAML={false}
                code={component.code}
              />
          )}
        </Grid>
      </Grid>
    );
  }
}
