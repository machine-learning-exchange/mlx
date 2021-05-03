// Copyright 2021 IBM Corporation 
// 
// Licensed under the Apache License, Version 2.0 (the "License"); 
// you may not use this file except in compliance with the License. 
// You may obtain a copy of the License at 
// 
//     http://www.apache.org/licenses/LICENSE-2.0 
// 
// Unless required by applicable law or agreed to in writing, software 
// distributed under the License is distributed on an "AS IS" BASIS, 
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
// See the License for the specific language governing permissions and 
// limitations under the License. 
import { SettingsPayload, AppSettings, Setting } from './types'

const ENDPOINT = '/settings'

function unpackSettingsPayload(payload: SettingsPayload): any {
  const [ endpoints, kfserving, capabilities, , artifacts ] = payload.sections

  return {
    endpoints:{
      api: endpoints.settings[0] as Setting<string>,
      kfp: endpoints.settings[1] as Setting<string>
    },
    kfserving: {
      namespace: kfserving.settings[0] as Setting<string>
    },
    capabilities: {
      upload: capabilities.settings[0] as Setting<boolean>,
      execute: capabilities.settings[1] as Setting<boolean>
    },
    artifacts: {
      pipelines: artifacts.settings[0] as Setting<boolean>,
      datasets: artifacts.settings[1] as Setting<boolean>,
      components: artifacts.settings[2] as Setting<boolean>,
      models: artifacts.settings[3] as Setting<boolean>,
      notebooks: artifacts.settings[4] as Setting<boolean>,
      workspace: artifacts.settings[5] as Setting<boolean>,
      inferenceservices: artifacts.settings[6] as Setting<boolean>,
    }
  }
}

export async function getSettings(uri: string): Promise<AppSettings> {
  try {
    const payload = await fetch(`${uri}${ENDPOINT}`, {
      headers: { Accept: 'application/json' }
    }).then((res: Response) => res.json())

    if (payload as SettingsPayload)
      return unpackSettingsPayload(payload)
    else
      throw Error(`Expected SettingsPayload but got ${payload}`)

  } catch (err) {
    throw Error(`Could not get settings. ${err}`)
  }
}

export async function updateSettings(uri: string, name: string, value: any): Promise<AppSettings> {
  const body = JSON.stringify({ [name]: value })
  const payload = await fetch(`${uri}${ENDPOINT}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json'
    },
    body
  }).then((res: Response) => res.json())

  if (payload as SettingsPayload)
    return unpackSettingsPayload(payload)
}

export async function resetSettings(
  uri: string, changes: { [prop: string]: any }
) {
  const payload = await fetch(`${uri}${ENDPOINT}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json'
    },
    body: JSON.stringify(changes)
  }).then((res: Response) => res.json())

  if (payload as SettingsPayload)
    return unpackSettingsPayload(payload)
}
