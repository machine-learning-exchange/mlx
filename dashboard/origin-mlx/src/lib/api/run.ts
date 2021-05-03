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

export interface RunParameters {
  name: string
  [prop: string]: any
}

function formatParameters(type: string, parameters: any) {
  switch (type) {
    case 'components':
      return Object.entries(parameters)
        .map(([ name, value ]) => ({ name, value }))
    case 'datasets':
      return Object.entries(parameters)
        .map(([ name, value ]) => ({ name, value }))
    default:
      return Object.fromEntries(Object.entries(parameters))
  }
}

export async function requestArtifactRun(
  API: string,
  type: string,
  id: string,
  parameters: RunParameters
) {
  const { runname, ...rest } = parameters
  const query = runname ? `?name=${runname}` : ''
  const response = await fetch(`${API}/apis/v1alpha1/${type}/${id}/run${query}`, {
    headers: {
      'Accept': 'application/json',
      'Content-type': 'application/json'
    },
    method: 'POST',
    body: JSON.stringify(formatParameters(type, rest))
  })

  return (response.status === 200) ? await response.json() : response.statusText
}

export async function requestPipelineRun(
  API: string,
  body_json: any
  ){
  
  const response = await fetch(`${API}/apis/v1alpha1/pipelines/run_custom_pipeline`, {
    headers: {
      'Accept': 'application/json',
      'Content-type': 'application/json'
    },
    method: 'POST',
    body: JSON.stringify(body_json)
  })

  return (response.status === 200) ? await response.json() : response.statusText
}
