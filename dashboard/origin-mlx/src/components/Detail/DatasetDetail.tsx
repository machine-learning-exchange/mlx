/* 
* Copyright 2021 The MLX Contributors
* 
* SPDX-License-Identifier: Apache-2.0
*/ 
import * as React from 'react';
import StoreContext from '../../lib/stores/context'

import SourceCodeDisplay from '../SourceCodeDisplay';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import yaml from 'js-yaml';
import { getUserInfo, hasRole } from '../../lib/util';
import RunView from '../RunView'
import RelatedAssetView from '../RelatedAssetView';
import MarkdownViewer from '../MarkdownViewer';
import LoadingMessage from '../LoadingMessage';
import MetadataView from '../MetadataView';

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
      leftTab: 'description',
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
      <div className="detail-wrapper">
        <Tabs
          variant="fullWidth"
          className="comp-tabs"
          value={ this.state.leftTab }
          onChange={(_, leftTab: string) => this.setState({ leftTab })}>
          <Tab 
            className="comp-tab"
            value="description" 
            label="Description" 
          />
          <Tab 
            className="comp-tab"
            value="source" 
            label="Dataset YAML"
          />
          { this.state.selectedGraphNode &&
            <Tab 
              className="comp-tab"
              value="component-code" 
              label={ `${ this.state.selectedGraphNode } Component` }
            />
          }
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
        <div className="detail-contents">
          { this.state.leftTab === 'description' &&
            <MarkdownViewer url={dataset.template.readme_url}></MarkdownViewer>
          }
          { this.state.leftTab === 'relatedAssets' &&
            <RelatedAssetView
              datasetId={dataset.id}
              relatedAssets={dataset.related_assets} 
              setRunLink={setRunLink}
            />
          }
          {this.state.leftTab === 'runCreation' &&
            <RunView type="datasets" asset={dataset} setRunLink={setRunLink}/>
          }
          { this.state.leftTab === "source" &&
            <SourceCodeDisplay 
              scrollMe={true}
              isYAML={true}
              code={dataset.yaml || ``}
            />
          }
          { this.state.leftTab === "component-code" &&
            <SourceCodeDisplay 
              scrollMe={true}
              isYAML={true}
              code={this.getComponentYAML(this.state.selectedGraphNode) || ``}
            />
          }
        </div>
      </div>
    )
  }
}
