// Copyright 2021 The MLX Contributors
// 
// SPDX-License-Identifier: Apache-2.0
import { State, Action } from './types'
import { Setting } from '../api/types'
import { withPersistence } from './util'
import merge from 'deepmerge'

export interface SettingsState extends State {
  branding: {
    name: Setting<string>
  },
  kfserving: {
    namespace: Setting<string>
  }
  endpoints: {
    api: Setting<string>,
    kfp: Setting<string>
  },
  capabilities: {
    upload: Setting<boolean>,
    execute: Setting<boolean>,
    edit: Setting<boolean>
  },
  artifacts: {
    pipelines: Setting<boolean>
    datasets: Setting<boolean>
    components: Setting<boolean>
    models: Setting<boolean>
    notebooks: Setting<boolean>
    inferenceservices: Setting<boolean>
  },
}

export function packSetting<T>(name: string, description: string, defaultValue: T, value?: T) {
  return { name, description, default: defaultValue, value }
}

const initial: SettingsState = {
  branding: {
    name: packSetting('App Name', 'Branding displayed in sidebar', 'My AIHub', process.env.REACT_APP_BRAND)
  },
  kfserving: {
    namespace: packSetting('Namespace', "Namespace to fetch the inference services from", '')
  },
  endpoints: {
    api: packSetting( 'API Endpoint', 'Machine Learning Exchange API Endpoint',
      process.env.REACT_APP_API
      ? `http${process.env.HTTPS ? 's' : ""}://${process.env.REACT_APP_API + (process.env.REACT_APP_BASE_PATH || "")}`
      : window.location.origin + (process.env.REACT_APP_BASE_PATH || "")),
    kfp: packSetting( 'KFP Endpoint', 'Kubeflow Pipelines API Endpoint',
      process.env.REACT_APP_KFP
      ? `http${process.env.HTTPS ? 's' : ""}://${process.env.REACT_APP_KFP}` 
      : window.location.origin)
  },
  capabilities: {
    // these should default to false in the wild
    upload: packSetting('Upload Enabled',
      'Allow the upload of artifacts', true),
    execute: packSetting('Execution Enabled',
      'Allow the execution of sample pipelines', true),
    edit: packSetting('Editing Enabled',
      'Allow the setting of featured artifacts and publishing approval', true)
  },
  artifacts: {
    datasets: packSetting('Datasets',
    'Enable or Disable the Datasets section', true),
    models: packSetting('Models',
      'Enable or Disable the Models section', true),
    pipelines: packSetting('Pipelines',
      'Enable or Disable the Pipelines section', true),
    components: packSetting('Components',
      'Enable or Disable the Components section', true),
    notebooks: packSetting('Notebooks',
      'Enable or Disable the Notebooks section', true),
    inferenceservices: packSetting('Inference Services',
      'Enable or Disable the Services section', true)
  }
}

export const GET_SETTINGS = 'GET_SETTINGS'
export const SET_SETTINGS = 'SET_SETTINGS'
export const RESET_SETTINGS = 'RESET_SETTINGS'

export interface GetSettingsAction extends Action {
  settings: SettingsState
}

export interface SetSettingsAction extends Action {
  settings: SettingsState
}

export interface ResetSettingsAction extends Action {}

export type SettingsAction = GetSettingsAction | SetSettingsAction
  | ResetSettingsAction

function keepDefault(key: any) {
  return (a: any, b: any) => {
    if (a.hasOwnProperty('default') && b.hasOwnProperty('default'))
      return { ...b, default: a.default }
    
    return merge(a, b, { customMerge: keepDefault })
  }
}

function reducer(state: State, action: Action) {
  if (action as SettingsAction) {
    switch (action.type) {
      case GET_SETTINGS: {
        const { settings } = action as GetSettingsAction
        // TODO: Remove when API is updated
        settings.endpoints.api = {
          "name": "API Endpoint",
          "description": "Machine Learning Exchange API endpoint",
          "value": settings.endpoints.api.value || "",
          "default": state.endpoints.api.default || ""
        }
        settings.endpoints.kfp = {
          "name": "KFP API",
          "description": "Kubeflow Pipelines API endpoint",
          "value": settings.endpoints.kfp.value || "",
          "default": state.endpoints.kfp.default || ""
        }
        return merge(state, settings, { customMerge: keepDefault })
      }
      case SET_SETTINGS: {
        const { settings } = action as SetSettingsAction
        // TODO: Remove when API is updated
        settings.endpoints.api = {
          "name": "API Endpoint",
          "description": "Machine Learning Exchange API endpoint",
          "value": settings.endpoints.api.value || "",
          "default": state.endpoints.api.default || ""
        }
        settings.endpoints.kfp = {
          "name": "KFP API",
          "description": "Kubeflow Pipelines API endpoint",
          "value": settings.endpoints.kfp.value || "",
          "default": state.endpoints.kfp.default || ""
        }
        return merge(state, settings)
      }
      case RESET_SETTINGS:
        return initial
      default:
        return state
    }
  }
}

export default withPersistence('settings', reducer)
export { initial as SettingsInitial }
