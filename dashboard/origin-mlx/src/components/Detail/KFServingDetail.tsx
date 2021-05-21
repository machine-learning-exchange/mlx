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
import SourceCodeDisplay from '../SourceCodeDisplay';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import yaml from 'js-yaml';
import CheckCircleIcon from '@material-ui/icons/CheckCircle';
import ErrorIcon from '@material-ui/icons/Error';
//import errorIcon from '../../images/error.png'
import closeButton from '../../images/close.png'
import updateIcon from '../../images/update-icon.png'

import Typography from '@material-ui/core/Typography';
import Button from '../../components/Button'
import Icon from '@material-ui/core/Icon'
import { upload } from '../../lib/api/upload'

import MetadataView from '../MetadataView';

import Popup from "reactjs-popup";

const isAdmin = hasRole(getUserInfo(), 'admin');

export interface KFServingDetailProps {
  API?: string
  namespace?: string
  setRunLink?: Function
  name?: string
  asset?: any
}

export interface KFServingDetailState {
  file?: File
  uploadStatus?: string
  topTab: string
  leftTab: string
  rightTab: string
  codeTab: string
  service: {
    template: any,
    yaml: string,
    [props: string]: any
  },
  isOpen: boolean

}

export default class KFServingDetail extends React.Component<KFServingDetailProps, KFServingDetailState> {
  static contextType = StoreContext

  constructor(props: any) {
    super(props);
    this.state = {
      topTab: 'info',
      rightTab: 'source',
      leftTab: 'detail',
      codeTab: '',
      service: props.asset,
      isOpen: false
    };
  }

  getCodeType = (tab:string) => {
    switch (tab) {
      case 'serve':
        return this.state.service.servable_tested_platforms
      case 'train':
        return this.state.service.trainable_tested_platforms
      default:
        return ['']
    }
  }

  getCode = (platform: string) =>
    this.state.service.code
      .find(({ execution_platform }: any) =>
        execution_platform === platform).script_code

  public render() {

    const API = this.props.API || ""
    const namespace = this.props.namespace || ""
    const service = this.state.service

    const handleFile = (e: React.ChangeEvent<HTMLInputElement>) => {
      this.setState({...this.state, file: e.currentTarget.files[0]})
    }

    const handleUpload = async () => {

      const file = this.state.file
      const response = await upload(API, 'inferenceservice', file, {})
      let uploadStatus = ""
      if (response.status < 200 || response.status >= 300) {
        uploadStatus = "Upload of " + file.name + " failed"
      }
      else{
        uploadStatus = "Upload Suceeded."
      }

      this.setState({...this.state, uploadStatus, file: null})
    }

    /////////////KIALI///////////////
    const kiali = `http${process.env.HTTPS ? 's' : ""}://${process.env.REACT_APP_KIALI}`
    const grafana = `http${process.env.HTTPS ? 's' : ""}://${process.env.REACT_APP_GRAFANA}`
    const kialiLink = `${kiali}/kiali/console/services?duration=60&namespaces=${namespace}&servicename=` + service.metadata.name + "&kiosk=true"
    const graphLink = `${kiali}/kiali/console/graph/namespaces/?edges=requestsPercentage&graphType=service&namespaces=${namespace}&unusedNodes=false&injectServiceNodes=true&duration=21600&refresh=10000&layout=dagre&kiosk=true`
    const grafanaLink = `${grafana}/d/UbsSZTDik/istio-workload-dashboard?orgId=1&var-namespace=${namespace}&var-workload=` + service.status.default.predictor.name + `-deployment&var-srcns=All&var-srcwl=All&var-dstsvc=All`

    /////////////PREDICTOR/////////////
    let predictorStatusIcon = <ErrorIcon className="error-icon"/>
    let predictorTimestamp = ""
    let predictorHost = ""

    /////////////EXPLAINER/////////////
    let explainerStatusIcon = <ErrorIcon className="error-icon"/>
    let explainerTimestamp = ""
    let explainerHost = ""
    //let explainerErrorIcon = ""
    let explainerReason = ""
    let explainerMessage = ""
    //let explainerSeverity = ""


    /////////////TRANSFORMER/////////////
    let transformerStatusIcon = <ErrorIcon className="error-icon"/>
    let transformerTimestamp = ""
    let transformerHost = ""
    //let transformerErrorIcon = ""
    let transformerReason = ""
    let transformerMessage = ""
    //let transformerSeverity = ""

    if (service.status) {
      for (let conditionIter=0; conditionIter<service.status.conditions.length; conditionIter++) {
        let condition = service.status.conditions[conditionIter]
        // If this is the DefaultPredictorReady status then scrape some info
        if (condition.type === "DefaultPredictorReady") {
          predictorTimestamp = condition.lastTransitionTime
          predictorHost = service.status.default.predictor.host
          if (condition.status === "True") {
            predictorStatusIcon = <CheckCircleIcon className="check-icon"/>
          }
        }
      }

      for (let conditionIter=0; conditionIter<service.status.conditions.length; conditionIter++) {
        let condition = service.status.conditions[conditionIter]
        if (condition.type === "DefaultExplainerReady") {
          explainerTimestamp = condition.lastTransitionTime
          if (condition.status === "True") {
            explainerStatusIcon = <CheckCircleIcon className="check-icon"/>
            explainerHost = service.status.default.transformer?.host || service.status.default.explainer.host
          }
          else {
            //explainerErrorIcon = errorIcon
            explainerReason = condition.reason
            explainerMessage = condition.message
            //explainerSeverity = condition.severity
          }
        }
      }

      for (let i=0; i<service.status.conditions.length; i++) {
        if (service.status.conditions[i].type === "DefaultTransformerReady") {
          transformerTimestamp = service.status.conditions[i].lastTransitionTime
          if (service.status.conditions[i].status === "True") {
            transformerStatusIcon = <CheckCircleIcon className="check-icon"/>
            transformerHost = service.status.default.transformer.host
          }
          else {
            //transformerErrorIcon = errorIcon
            transformerReason = service.status.conditions[i].reason
            transformerMessage = service.status.conditions[i].message
            //transformerSeverity = service.status.conditions[i].severity
          }
        }
      }
    }
  
    return (
      <>
        <Tabs 
          variant="fullWidth"
          className="comp-tabs" 
          value={ this.state.topTab }
          onChange={(_, value: string) => this.setState({ topTab: value })}
        >
          <Tab 
            className="comp-tab"
            value="info" 
            label="Information" 
          />
          <Tab 
            className="comp-tab"
            value="kiali" 
            label="Traffic Info" 
          />
          <Tab 
            className="comp-tab"
            value="grafana" 
            label="Grafana" 
          />
          <Tab 
            className="comp-tab"
            value="graph" 
            label="Graph" 
          />
        </Tabs>
        { this.state.topTab === "info" &&
          <Grid
            className="detail-content"
            container
            spacing={ 0 } 
            justify="center"
          >
            <Grid 
              className="left-wrapper"
              item xs={ 6 }
            >
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
                </Tabs>
              </div>
              {this.state.leftTab === 'detail' &&
                <div style={{overflow: "auto"}}>
                  <MetadataView content={{
                      Overview: [
                        { name: "Service Name", data: capitalize(service.metadata.name)},
                        { name: "Resource Version", data: service.metadata.resourceVersion },
                        { name: "Traffic", data: service.status.canaryTraffic ? String(100 - parseInt(service.status.canaryTraffic)) : "" },
                        { name: "Canary Traffic", data: service.status.canaryTraffic || "" }
                      ]
                    }}
                  />
                  <div style={{ overflow: 'none', height: 'auto', padding: '0.5rem' }}>
                    <Typography 
                      variant="h5" 
                      className="inputs-label">
                      Configure KFServices 
                    </Typography>
                  </div>
                  <div className="filePicker-wrapper detail-button">
                    { isAdmin && (!this.state.file ?
                      <>
                        <Button
                          className="hero-buttons upload-button" 
                          variant="contained" 
                          color="primary">
                          <Icon>cloud_upload</Icon>
                          {` Select File`}
                        </Button>
                        <input 
                          type="file" 
                          name="component-file"
                          onChange={handleFile}
                          accept=".tgz, .gz"
                        />
                        <p>{this.state.uploadStatus}</p>
                      </>
                    :
                    <>
                      <Button 
                        className="hero-buttons upload-button" 
                        variant="contained" 
                        color="primary"
                        type="submit"
                        onClick={handleUpload}
                      >
                        <Icon>cloud_upload</Icon>
                        {`Upload`}
                      </Button>
                      <p>{this.state.file.name}</p>
                    </>
                    )}
                  </div>
                  { predictorTimestamp &&
                    <MetadataView 
                      content={{
                        Predictor: [
                          { name: "Timestamp", data: predictorTimestamp},
                          { name: "Host", data: predictorHost }
                        ]
                      }}
                      titleIcon={predictorStatusIcon}
                    />
                  }
                  { explainerTimestamp && 
                    <MetadataView 
                      content={{
                        Explainer: [
                          { name: "Timestamp", data: explainerTimestamp},
                          { name: "Status", data: explainerReason },
                          { name: "Host", data: explainerHost },
                          { name: "Message", data: explainerMessage}
                        ]
                      }}
                      titleIcon={explainerStatusIcon}
                    />
                  }
                  { transformerTimestamp && 
                    <MetadataView 
                      content={{
                        Transformer: [
                          { name: "Timestamp", data: transformerTimestamp},
                          { name: "Status", data: transformerReason },
                          { name: "Host", data: transformerHost },
                          { name: "Message", data: transformerMessage}
                        ]
                      }}
                      titleIcon={transformerStatusIcon}
                    />
                  }
                </div>
              }
              {/* Temporarily remove for first pass (using 'false && ') */}
              { false &&
                <Popup trigger={<button style={{paddingTop: '10px', paddingBottom: '10px', border: 'none', outline: 'none', fontSize: '14px', marginTop: '20px', backgroundColor: '#1BCDC7', color: 'white', width: '620px'}}> <img src={updateIcon} style={{width: '15px', height: 'auto', marginBottom: '-3px', marginRight: '8px'}} alt=""/>UPDATE SERVICE</button>} position="top center" contentStyle={{ marginTop: '30px', marginLeft: '300px', width: '1165px', height: '670px', zIndex: 100, opacity: 1, boxShadow: '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)', borderWidth: '5px', borderColor: '#1BCDC7' }} arrow={false}>
                    <div style={{position: 'relative'}}>
                      <a href={service.metadata.name} className="close" style={{color: '#1BCDC7', zIndex: 300, position: 'absolute'}}>
                        <img alt="close button" src={closeButton} style={{width: '25px', height: 'auto', zIndex: 300}}/>
                      </a>
                    </div>
                </Popup>
              }
            </Grid>
            <Grid 
              className="right-wrapper"
              item xs={ 6 }
            >
              <div className="tab-nav">
                <Tabs 
                  variant="fullWidth"
                  className="comp-tabs" 
                  value={ this.state.rightTab }
                  onChange={(_, value: string) => this.setState({
                    rightTab: value,
                    codeTab: this.getCodeType(value)[0]
                  })}
                >
                  <Tab 
                    className="comp-tab"
                    value="source" 
                    label="YAML Definition"
                  />
                </Tabs>
              </div>
              { (this.state.rightTab === "train" || this.state.rightTab === "serve") &&
                <div className="tab-nav second-row">
                  <Tabs
                    variant="fullWidth"
                    className="comp-tabs second-row" 
                    value={this.state.codeTab || this.setState({
                      codeTab: this.getCodeType(this.state.rightTab)[0]
                    })}
                    onChange={(_, value: string) => this.setState({ codeTab: value })}
                  >
                    {this.getCodeType(this.state.rightTab).map((platform: string) =>
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
              {this.state.rightTab === "source" &&
                <SourceCodeDisplay 
                  isYAML={ true }
                  code={yaml.safeDump(service)}
                />
              }
            </Grid>            
          </Grid>
        }
        { this.state.topTab === "kiali" && 
          <iframe title="kiali" className="service-iframe" src={kialiLink}></iframe>
        }
        { this.state.topTab === "grafana" && 
          <iframe title="grafana" className="service-iframe" src={grafanaLink}></iframe>
        }
        { this.state.topTab === "graph" && 
          <iframe title="graph" className="service-iframe" src={graphLink}></iframe>
        }
      </>
    )
  }
}