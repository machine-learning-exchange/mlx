/*
* Copyright 2021 The MLX Contributors
*
* SPDX-License-Identifier: Apache-2.0
*/
import * as React from 'react';
import Grid from '@material-ui/core/Grid';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Typography from '@material-ui/core/Typography';
import StoreContext from '../../lib/stores/context';
import { getUserInfo, hasRole } from '../../lib/util';

import SourceCodeDisplay from '../SourceCodeDisplay';
import RunView from '../RunView';
import LoadingMessage from '../LoadingMessage';
import MetadataView from '../MetadataView';

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

function purifyData(data: any, defaultString: string): string {
  if (typeof data === 'string') return data;
  return defaultString;
}

export default class ComponentDetail extends React.Component<ComponentDetailProps, ComponentDetailState> {
  static contextType = StoreContext;

  constructor(props: any) {
    super(props);
    this.state = {
      rightTab: 'source',
      leftTab: 'detail',
      component: props.asset,
    };
  }

  async componentDidMount() {
    const { store } = this.context;
    const { api } = store.settings.endpoints;
    const API = api.value || api.default;

    const { component } = this.state;
    const codeRes = await fetch(`${API}/apis/v1alpha1/components/${component.id}/generate_code`);

    this.setState({
      component: {
        ...component,
        code: (await codeRes.json()).script,
      },
    });
  }

  public render() {
    const { store } = this.context;
    const { execute } = store.settings.capabilities;
    const canRun = execute.value !== null ? execute.value : execute.default;
    const { setRunLink } = this.props;

    const { component } = this.state;

    return (
      <Grid
        container
        spacing={0}
        justify="center"
      >
        <Grid
          className="left-wrapper"
          item
          xs={6}
        >

          <div className="tab-nav">
            <Tabs
              variant="fullWidth"
              className="comp-tabs"
              value={this.state.leftTab}
              onChange={(_, leftTab: string) => this.setState({ leftTab })}
            >
              <Tab
                className="comp-tab"
                value="detail"
                label="Details"
              />
              {canRun && isAdmin
                && (
                <Tab
                  className="comp-tab"
                  value="runCreation"
                  label="Launch"
                />
                )}
            </Tabs>
          </div>
          {this.state.leftTab === 'detail'
            && (
            <MetadataView
              content={{
                inputs: component.template.inputs,
                outputs: component.template.outputs,
                arguments: [
                  <span
                    className="args"
                    style={{
                      maxWidth: '90% !important',
                    }}
                  >
                    <Typography
                      className="arg-heavy"
                      variant="h6"
                      inline
                    >
                      {
                        purifyData(component.template.implementation.container.command, 'python ')
                      }
                    </Typography>
                    {(component.template.implementation.container.args || []).map((arg: any, i: number) => ((typeof arg === 'string')
                      ? (
                        <Typography
                          key={arg + i}
                          className="arg-heavy"
                          variant="h6"
                          inline
                        >
                          {`${arg} `}
                        </Typography>
                      )
                      : (
                        <i key={arg.inputValue + i}>
                          <Typography
                            className="arg-light"
                            variant="subheading"
                            inline
                          >
                            {`${arg.inputValue || arg.outputPath} `}
                          </Typography>
                        </i>
                      )))}
                    <div style={{ height: '2rem' }} />
                  </span>,
                  { name: 'command', description: purifyData(component.template.implementation.container.command, 'python ') },
                  { name: 'image', description: purifyData(component.template.implementation.container.image, '') },
                ],
              }}
            />
            )}
          { this.state.leftTab === 'runCreation'
            && <RunView type="components" asset={component} setRunLink={setRunLink} />}
        </Grid>
        <Grid
          className="right-wrapper"
          item
          xs={6}
        >
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
              <Tab
                className="comp-tab"
                value="sample"
                label="Sample Pipeline Code"
              />
            </Tabs>
          </div>
          {this.state.rightTab === 'source' && (
            <SourceCodeDisplay
              isYAML
              code={component.yaml}
            />
          )}
          {this.state.rightTab === 'sample' && (!component.code
            ? <LoadingMessage message="Loading component code..." />
            : (
              <SourceCodeDisplay
                isYAML={false}
                code={component.code}
              />
            )
          )}
        </Grid>
      </Grid>
    );
  }
}
