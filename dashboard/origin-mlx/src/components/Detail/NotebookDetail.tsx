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

import DataList from '../DataList';
import Grid from '@material-ui/core/Grid';
import SourceCodeDisplay from '../SourceCodeDisplay';
import RunView from '../RunView'
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';

const isAdmin = hasRole(getUserInfo(), 'admin');

export interface INotebookDetailProps {
  setRunLink?: Function
  name?: string
  asset?: any
}

export interface NotebookDetailState {
  notebook: {
    url: string
    template: any,
    yaml: string,
    [props: string]: any
  }
  leftTab: string;
  rightTab: string;
}

export default class NotebookDetail extends React.Component<INotebookDetailProps, any> {
  static contextType = StoreContext

  constructor(props: any) {
    super(props);
    this.state = {
      rightTab: 'source',
      leftTab: 'detail',
      notebook: props.asset,
    }
  }

  public render() {
    const { store } = this.context
    const { execute } = store.settings.capabilities
    const canRun = execute.value !== null ? execute.value : execute.default
    const setRunLink = this.props.setRunLink

    const notebook = this.state.notebook;

    const viewerUrl = notebook.url &&
      `${notebook.url.includes('github.com')
        ? 'https://nbviewer.jupyter.org/url/'
        : 'http://' + process.env.REACT_APP_NBVIEWER_API + '/url/'}`
      + notebook.url.match(/https?:\/\/(.*)/)[1]

    return (
      <Grid
        container
        spacing={ 0 }
        justify="center"
      >
        <Grid
          className="left-wrapper"
          item xs={ 6 }>
          <div className="tab-nav">
            <Tabs
              variant="fullWidth"
              className="comp-tabs"
              value={this.state.leftTab}
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
          { this.state.leftTab === 'detail' &&
            <div className="component-detail-side">
              <span>
                <DataList
                  title="About:"
                  items={[
                    {
                      name: "name",
                      data: notebook.name
                    },
                    {
                      name: "description",
                      data: notebook.description
                    },
                    {
                      name: "platform",
                      data: notebook.metadata.annotations.platform
                    },
                  ]}
                />
                <DataList
                  title="Implementation:"
                  items={[
                    {
                      name: "github",
                      data: notebook.template.implementation.github.source,
                      itemClass: "model-link"
                    },
                  ]}
                />
              </span>
            </div>
          }
          { this.state.leftTab === 'runCreation' &&
            <RunView type="notebooks" asset={notebook} setRunLink={setRunLink}/>}
        </Grid>
        <Grid
          className="right-wrapper"
          item xs={ 6 }>
          <div className="tab-nav">
          <Tabs
            variant="fullWidth"
            className="comp-tabs"
            value={this.state.rightTab}
            onChange={(_, rightTab: string) => this.setState({ rightTab })}
          >
            <Tab
              className="comp-tab"
              value="source"
              label="YAML Definition"
            />
            {viewerUrl &&
              <Tab
                  className="comp-tab"
                  value="notebook"
                  label="NOTEBOOK CODE"
              />
            }
          </Tabs>
          </div>
          {this.state.rightTab === 'source' &&
            <SourceCodeDisplay
              isYAML={ true }
              code={notebook.yaml || ``}
            />
          }
          {this.state.rightTab === 'notebook' &&
            <iframe style={{height: '100%'}} title="Notebook Viewer" src={viewerUrl}></iframe>}
        </Grid>
      </Grid>
    );
  }
}
