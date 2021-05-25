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

import Grid from '@material-ui/core/Grid';
import LoadingMessage from '../LoadingMessage';
import RunView from '../RunView'
import SourceCodeDisplay from '../SourceCodeDisplay';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import yaml from 'js-yaml';
import MetadataView from '../MetadataView';
import RelatedAssetView from '../RelatedAssetView';
import { getUserInfo, hasRole } from '../../lib/util';

const isAdmin = hasRole(getUserInfo(), 'admin');

export interface IPipelineDetailProps {
  setRunLink?: Function
  name?: string
  asset?: any
}

export default class PipelineDetail extends React.Component<IPipelineDetailProps, any> {
  static contextType = StoreContext

  constructor(props: any) {
    super(props);
    this.state = {
      rightTab: 'source',
      leftTab: 'detail',
      selectedGraphNode: '',
      dataset: props.asset
    }
  }

  getComponentYAML = (name:string) => {
    const nodeCode = this.state.pipeline.template.spec.templates
      .find((container:any) => 
        container.name.includes(name.slice(0, name.length - (name.includes('...') && 3))))
    return yaml.safeDump(nodeCode)
  }
  
  public render() {
    const { store } = this.context
    const { execute } = store.settings.capabilities
    const canRun = execute.value !== null ? execute.value : execute.default

    const dataset = this.state.dataset
    const setRunLink = this.props.setRunLink

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
              { dataset.related_assets && dataset.related_assets.length !== 0 &&
                <Tab
                  className="comp-tab"
                  value="relatedAssets"
                  label="Related Assets"
                />
              }
            </Tabs>
          </div>
          { this.state.leftTab === 'detail' &&
            <div className="component-detail-side">
              {!dataset.yaml
                ? <LoadingMessage message="Loading Pipeline details..." />
                : <MetadataView 
                    content={{
                      about: [
                        { name: "Source", data: dataset.template.source.name },
                        { name: "Data Format", data: dataset.template.format[0].type },
                        { name: "License", data: dataset.license },
                        { name: "Number of records", data: dataset.number_of_records.toString() },
                        { name: "Version", data: dataset.template.version },
                        { name: "Created at", data: dataset.created_at },
                        { name: "Description", data: dataset.description },
                      ]
                    }}
                  />
              }
            </div>
          }
          {this.state.leftTab === 'runCreation' &&
            <RunView type="datasets" asset={dataset} setRunLink={setRunLink}/>
          }
          { this.state.leftTab === 'relatedAssets' &&
            <RelatedAssetView
              datasetId={dataset.id}
              relatedAssets={dataset.related_assets} 
              setRunLink={setRunLink}
            />
          }
        </Grid>
        <Grid 
          className="right-wrapper"
          item xs={ 6 }>
          <div className="tab-nav">
            <Tabs 
              variant="fullWidth"
              className="comp-tabs" 
              value={ this.state.rightTab }
              onChange={(_, rightTab: string) => this.setState({ rightTab })}>
              <Tab 
                className="comp-tab"
                value="source" 
                label="Pipeline YAML"
              />
              { this.state.selectedGraphNode &&
                <Tab 
                  className="comp-tab"
                  value="component-code" 
                  label={ `${ this.state.selectedGraphNode } Component` }
                />
              }
            </Tabs>
          </div>

          { this.state.rightTab === "source" &&
            <SourceCodeDisplay 
              scrollMe={true}
              isYAML={true}
              code={dataset.yaml || ``}
            />
          }

          { this.state.rightTab === "component-code" &&
            <SourceCodeDisplay 
              scrollMe={true}
              isYAML={true}
              code={this.getComponentYAML(this.state.selectedGraphNode) || ``}
            />
          }

        </Grid>
      </Grid>
    )
  }
}
