/*
* Copyright 2021 The MLX Contributors
*
* SPDX-License-Identifier: Apache-2.0
*/
import * as React from 'react';

import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import yaml from 'js-yaml';
import SourceCodeDisplay from '../SourceCodeDisplay';
import StoreContext from '../../lib/stores/context';
import { getUserInfo, hasRole } from '../../lib/util';
import RunView from '../RunView';
import RelatedAssetView from '../RelatedAssetView';
import MarkdownViewer from '../MarkdownViewer';
import MetadataView from '../MetadataView';

const isAdmin = hasRole(getUserInfo(), 'admin');

export interface IPipelineDetailProps {
  setRunLink?: Function
  name?: string
  asset?: any
}

export default class PipelineDetail extends React.Component<IPipelineDetailProps, any> {
  static contextType = StoreContext;

  constructor(props: any) {
    super(props);
    this.state = {
      rightTab: 'source',
      leftTab: 'description',
      selectedGraphNode: '',
      dataset: props.asset,
    };
  }

  getComponentYAML = (name:string) => {
    const nodeCode = this.state.pipeline.template.spec.templates
      .find((container:any) => container.name.includes(name.slice(0, name.length - (name.includes('...') && 3))));
    return yaml.safeDump(nodeCode);
  };

  public render() {
    const { store } = this.context;
    const { execute } = store.settings.capabilities;
    const canRun = execute.value !== null ? execute.value : execute.default;

    const { dataset } = this.state;
    const { setRunLink } = this.props;

    return (
      <div className="detail-wrapper">
        <Tabs
          variant="fullWidth"
          className="comp-tabs"
          value={this.state.leftTab}
          onChange={(_, leftTab: string) => this.setState({ leftTab })}
        >
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
          { this.state.selectedGraphNode
            && (
            <Tab
              className="comp-tab"
              value="component-code"
              label={`${this.state.selectedGraphNode} Component`}
            />
            )}
          {canRun && isAdmin
            && (
            <Tab
              className="comp-tab"
              value="runCreation"
              label="Launch"
            />
            )}
          { dataset.related_assets && dataset.related_assets.length !== 0
            && (
            <Tab
              className="comp-tab"
              value="relatedAssets"
              label="Related Assets"
            />
            )}
        </Tabs>
        <div className="detail-contents">
          { this.state.leftTab === 'description' && ((dataset.template && dataset.template.readme_url)
            ? <MarkdownViewer url={dataset.template.readme_url} />
            : (
              <MetadataView
                content={{
                  about: [
                    { name: 'Source', data: dataset.template.source.name },
                    { name: 'Data Format', data: dataset.template.format[0].type },
                    { name: 'License', data: dataset.license },
                    { name: 'Number of records', data: dataset.number_of_records.toString() },
                    { name: 'Version', data: dataset.template.version },
                    { name: 'Created at', data: dataset.created_at },
                    { name: 'Description', data: dataset.description },
                  ],
                }}
              />
            )
          )}
          { this.state.leftTab === 'relatedAssets'
            && (
            <RelatedAssetView
              datasetId={dataset.id}
              relatedAssets={dataset.related_assets}
              setRunLink={setRunLink}
            />
            )}
          {this.state.leftTab === 'runCreation'
            && <RunView type="datasets" asset={dataset} setRunLink={setRunLink} />}
          { this.state.leftTab === 'source' && (
            <SourceCodeDisplay
              scrollMe
              isYAML
              code={dataset.yaml || ''}
            />
          )}
          { this.state.leftTab === 'component-code' && (
            <SourceCodeDisplay
              scrollMe
              isYAML
              code={this.getComponentYAML(this.state.selectedGraphNode) || ''}
            />
          )}
        </div>
      </div>
    );
  }
}
