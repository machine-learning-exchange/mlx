/*
* Copyright 2021 The MLX Contributors
*
* SPDX-License-Identifier: Apache-2.0
*/
import * as React from 'react';
import StoreContext from '../lib/stores/context'
import { updateSettings, resetSettings } from '../lib/api/settings';
import { SET_SETTINGS } from '../lib/stores/settings';
import { resetCache } from '../lib/api/artifacts';

import Hero from '../components/Hero'
import Link from '../components/Link'
import Button from '../components/Button'
import DataList from '../components/DataList';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import Icon from '@material-ui/core/Icon';
import InputAdornment from '@material-ui/core/InputAdornment';
import IconButton from '@material-ui/core/IconButton';

import { importCatalog } from '../lib/api/upload'

const SECRET_PW = 'mlx4codait'

export interface ISettingsPageProps {
  // API_ENDPOINT: string;
  // savedSettings: any;
  // setOption: Function;
  // setAllOptions: Function;
  alternateBG?: boolean;
}

export interface IAppSettingsObject {
  sections: Array<{ settings: Array<ISettingsObject> }>;
}

interface ISettingsObject {
  name: string;
  description: string;
  default: string;
  value: string;
}

export class SettingsPage extends React.Component<ISettingsPageProps, any> {
  static contextType = StoreContext

  constructor(props: ISettingsPageProps) {
    super(props)

    this.state = {
      textField: {
        API: '',
        KFP: '',
        namespace: ''
      },
      secret: '',
      showBody: true,
      showSecret: false
    }

  }

  componentDidMount = async () => {
    const { store } = this.context
    const { api, kfp } = store.settings.endpoints
    const API = api.value || api.default
    const KFP = kfp.value || kfp.default

    this.setState({
      textField: { API, KFP }
    })
  }

  apply = (name: string, value: string) => {
    const { store, dispatch } = this.context
    let API = store.settings.endpoints.api.value || store.settings.endpoints.api.default

    if (name === 'API Endpoint')
      API = value

    updateSettings(`${API}/apis/v1alpha1`, name, value)
      .then(settings => dispatch({ type: SET_SETTINGS, settings }))
  }

  // applySettings = (newSettings:IAppSettingsObject) => {
  //   this.setState({
  //     API: newSettings.sections[0].settings[0] || process.env.REACT_APP_API,
  //     KFP: newSettings.sections[0].settings[1] || process.env.REACT_APP_KFP,
  //     upload: newSettings.sections[1].settings[0],
  //     execution: newSettings.sections[1].settings[1],
  //     numFeatured: newSettings.sections[2].settings[0],
  //     savedSettings: newSettings,
  //     textField: {
  //       API: newSettings.sections[0].settings[0].value || process.env.REACT_APP_API,
  //       KFP: newSettings.sections[0].settings[1].value || process.env.REACT_APP_KFP
  //     },
  //   })
  // }

  // loadSettings = async () => {
  //   const API_ENDPOINT = this.props.API_ENDPOINT || process.env.REACT_APP_API;

  //   let settings:IAppSettingsObject = { sections: [] };
  //   if (this.props.savedSettings) {
  //     settings = this.props.savedSettings
  //   } else {
  //     const settingsReq = await fetch(`http://${ API_ENDPOINT }/apis/v1alpha1/settings`, {
  //       headers: {
  //         'Accept': 'application/json'
  //       }
  //     });
  //     settings = await settingsReq.json();
  //   }
  //   return settings;
  // }

  handleToggle = (name: string) => async (event: any) =>
    this.apply(name, event.currentTarget.checked)

  handleSelect = (name: string) => async (event: any) =>
    this.apply(name, event.currentTarget.value)

  handleText = (name: string) => async (event:any) => {
    if (name === 'API Endpoint') {
      this.setState({
        textField: {
          ...this.state.textField,
          API: event.target.value
        }
      })
    } else if (name === 'KFP API') {
      this.setState({
        textField: {
          ...this.state.textField,
          KFP: event.target.value
        }
      })
    } else if (name === 'secret') {
      this.setState({
        secret: event.target.value
      })
    } else if (name === 'Namespace') {
      this.setState({
        textField: {
          ...this.state.textField,
          namespace: event.target.value
        }
      })
    }
  }

  handleFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const fileReader = new FileReader()
    this.setState({progress: 0})
    fileReader.onloadend = async (e) => {
      const { store } = this.context
      let API = store.settings.endpoints.api.value || store.settings.endpoints.api.default
      const text : any = (e.target.result)
      const json = JSON.parse(text)
      const apiTokens = json["api_access_tokens"]

      let itemIter = 0
      const fullLength = json.components.length + json.datasets.length + json.models.length + json.notebooks.length + json.pipelines.length
      const addProgress = () => {
        itemIter += 1
        this.setState({progress: Math.round(100*itemIter/fullLength)})
      }

      for(const artifactType of Object.keys(json)) {
        if (artifactType !== "api_access_tokens") {
          const artifact = json[artifactType]
          for(const item of artifact) {
            importCatalog(API, JSON.stringify({"api_access_tokens": apiTokens, [artifactType]: [item]}))
              .then(addProgress)
          }
        }
      }
    }
    fileReader.readAsText(e.currentTarget.files[0])
  }

  saveText = (name:string) => async (event:any) => {
    let value = ''
    if (name === 'API Endpoint') {
      value = this.state.textField.API;
    } else if (name === 'KFP API') {
      value = this.state.textField.KFP;
    } else if (name === 'Namespace') {
      value = this.state.textField.namespace
    }
    this.apply(name, value)
  }

  reset = async () => {
    const { store, dispatch } = this.context
    const API = store.settings.endpoints.api.value || store.settings.endpoints.api.default

    const changes = Object.values(this.context.store.settings).map(section => {
      return Object.values(section).map((setting) => [ setting.name, setting.default ])
    }).flat()

    resetSettings(`${API}/apis/v1alpha1`, Object.fromEntries(changes))
      .then(settings => dispatch({ type: SET_SETTINGS, settings }))
  }

  // setDefaults = async () => {
  //   const defaultState = this.state.savedSettings;
  //   defaultState.sections.forEach((section:any, s:number) => {
  //     section.settings.forEach((setting:any, i:number) => {
  //       setting.value = setting.default;
  //     })
  //   })
  //   const newSettings = await this.props.setAllOptions(defaultState);
  //   this.applySettings(newSettings);
  // }

  // getArtifactList = () => {
  //   let maxIndex = this.state.execution.value === true ? 6 : 5;

  //   const aList = this.state.savedSettings.sections[3].settings
  //     .slice(0, maxIndex)
  //     .map((aType:any, i:number) => {
  //       return ({
  //         itemClass: "toggle-switch",
  //         name: aType.name,
  //         data: aType.value,
  //         thirdColData: aType.description,
  //         handleClick: this.handleToggle
  //       })
  //     })
  //   return aList;
  // }

  toggleShowPassword = () => {
    this.setState({
      showSecret: !this.state.showSecret
    })
  }

  passwordCheck = () => {
    if (this.state.secret === SECRET_PW) {
      this.setState({
        showBody: true
      })
    }
  }

  public render() {
    const { store } = this.context
    const { branding, kfserving, endpoints, capabilities, artifacts } = store.settings
    const name = branding.name.value || branding.name.default

    return (
      <div className="page-wrapper">
        <>
          <Hero
            title="Settings"
            subtitle={`Adjust ${name} Settings here.`}
            alternate={this.props.alternateBG}
          >
            <Link to={'/'}>
              <Button
                className="hero-buttons-outline"
                variant="outlined"
                color="primary"
              >
                {<Icon>arrow_back</Icon>}
                Home
              </Button>
            </Link>
          </Hero>
          <div className="settings-wrapper">
          {this.state.showBody ?
            <div className="settings-body">
              <DataList
                title="Bulk Imports:"
                items={[
                  {
                    itemClass: "file-button",
                    name: "Catalog Import",
                    data: this.state.textField.API,
                    savedValue: endpoints.api.value,
                    thirdColData: "Import artifacts from a JSON file",
                    handleFile: this.handleFile,
                    progress: this.state.progress
                  },
                ]}
              />
              <DataList
                title="KFServing Settings:"
                items={[
                  {
                    itemClass: "text-input",
                    name: kfserving.namespace.name,
                    data: this.state.textField.namespace,
                    savedValue: kfserving.namespace.value,
                    thirdColData: kfserving.namespace.description,
                    handleType: this.handleText,
                    saveValue: this.saveText
                  },
                ]}
              />
              <DataList
                title="Capabilities:"
                items={[
                  {
                    itemClass: "toggle-switch",
                    name: capabilities.upload.name,
                    data: capabilities.upload.value,
                    thirdColData: capabilities.upload.description,
                    handleClick: this.handleToggle
                  },
                  {
                    itemClass: "toggle-switch",
                    name: capabilities.execute.name,
                    data: capabilities.execute.value,
                    thirdColData: capabilities.execute.description,
                    handleClick: this.handleToggle
                  }
                ]}
              />
              {/* <DataList
                title="Appearance:"
                items={[
                  {
                    itemClass: "drop-down",
                    name: this.state.numFeatured.name,
                    data: this.state.numFeatured.value,
                    options: [10, 15],
                    thirdColData: this.state.numFeatured.description,
                    handleSelect: this.handleSelect
                  },
                ]}
              />  */}
              <DataList
                title="Cache Settings:"
                items={[
                  {
                    itemClass: "button",
                    name: "Reset Cache",
                    thirdColData: "Invalidate all cache entries",
                    handleClick: resetCache
                  },
                ]}
              />
              <DataList
                title="Artifact Types:"
                items={Object.values(artifacts).map((setting: any) => ({
                  itemClass: "toggle-switch",
                  name: setting.name,
                  data: setting.value,
                  thirdColData: setting.description,
                  handleClick: this.handleToggle
                }))}
              />

              <div className="default-btn-wrapper">
                <Button
                  className="hero-buttons"
                  variant="contained"
                  onClick={this.reset}>
                    Reset Defaults
                </Button>
              </div>
            </div>
          :
            <div className="loading-wrapper">
              <Typography variant="subtitle1">
                { `Enter Password to Access Settings` }
              </Typography>
              <TextField
                type={ this.state.showSecret ? "text" : "password" }
                className="password-text"
                value={ this.state.secret }
                onChange={ this.handleText('secret') }
                margin="dense"
                variant="outlined"
                autoCorrect="false"
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">
                      <IconButton
                        aria-label="Toggle password visibility"
                        onClick={ this.toggleShowPassword }>
                        { this.state.showSecret === true ? <Icon>visibility_off</Icon> : <Icon>visibility</Icon> }
                      </IconButton>
                    </InputAdornment>
                  )
                }}
              />
              <Button
                className="hero-buttons password-button"
                variant="contained"
                color="primary"
                onClick={ this.passwordCheck }>
                <Icon>build</Icon>
                { `Access Settings` }
              </Button>
            </div>
          }
          </div>
        </>
      </div>
    );
  }
}

export default SettingsPage
