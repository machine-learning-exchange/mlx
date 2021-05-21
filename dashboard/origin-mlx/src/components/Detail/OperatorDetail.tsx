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
import { getUserInfo, hasRole } from '../../lib/util'

import Grid from '@material-ui/core/Grid';
import ReactMarkdown from 'react-markdown';
import RunView from '../RunView'
import SourceCodeDisplay from '../SourceCodeDisplay';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';

const isAdmin = hasRole(getUserInfo(), 'admin');

export interface IOperatorDetailProps {
  setRunLink?: Function
  name?: string
  asset?: any
}

export interface OperatorDetailState {
  operator: {
    templates: {
      [kind: string]: { raw: string, template: any, url: string }
    }[],
    [props: string]: any
  }
  leftTab: string
  rightTab: string
}

export default class OperatorDetail extends React.Component<IOperatorDetailProps, any> {
  static contextType = StoreContext

  constructor(props: any) {
    super(props);
    this.state = {
      rightTab: 'Definition',
      leftTab: 'detail',
      operator: props.asset,
    }
  }

  public render() {
    const { store } = this.context
    const { execute } = store.settings.capabilities
    const canRun = execute.value !== null ? execute.value : execute.default

    const operator = this.state.operator
    const setRunLink = this.props.setRunLink

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
                  label="Install" 
                />
              }
            </Tabs>
          </div>
          {this.state.leftTab === 'detail' &&
            <div className="component-detail-side">
              <ReactMarkdown source={
                `## ${operator.name}\n` +
                operator.description + '\n' +
                `### Running This Operator\n` +
                `For instructions to run this operator, see [this page](${operator.url}#readme).`
              }/>
            </div>
          }
          {this.state.leftTab === 'runCreation' &&
            <RunView type="operators" asset={operator} setRunLink={setRunLink}/>}
        </Grid>
        <Grid 
          className="right-wrapper"
          item xs={ 6 }>
          <div className="tab-nav">
            <Tabs 
              variant="fullWidth"
              className="comp-tabs" 
              value={ this.state.rightTab }
              onChange={(_, value: string) => this.setState({ rightTab: value })}
            >
              <Tab 
                className="comp-tab"
                value="Definition" 
                label="YAML Definition"
              />
              <Tab 
                className="comp-tab"
                value="ClusterServiceVersion" 
                label="Cluster Service Version"
              />
              <Tab 
                className="comp-tab"
                value="CustomResourceDefinition" 
                label="Custom Resource Definition"
              />
            </Tabs>
          </div>
            {Object.entries(operator.templates).filter(([ name, _ ]: any) => this.state.rightTab === name)
              .map(([ name, template ]: any) =>
                <SourceCodeDisplay key={name} isYAML={ true } code={template.raw || ''} />
              )
            }
        </Grid>
      </Grid>
    )
  }
}
