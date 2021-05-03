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
import { Artifact } from '../stores/artifacts'

const supported = [
  'pipelines',
  'datasets',
  'components',
  'models',
  'operators',
  'notebooks',
  'inferenceservices'
]

const mocked: any[] = [
  // 'notebooks'
]

export async function fetchArtifact(API: string, type: string, namespace?: string) {
  if (!supported.includes(type) && !mocked.includes(type))
    throw Error(`Can't fetch assets for type <${type}>. Unsupported.`)

  console.log(`fetching assets for ${type}`)

  const response = type === "inferenceservices"
    ? await fetch(`${API}/apis/v1alpha1/${type}${namespace ? `?namespace=${namespace}` : ''}`)
    : await fetch(`${API}/apis/v1alpha1/${type}`)
  let assets = (await response.text().then(JSON.parse))

  assets = (type === "inferenceservices" ? assets.items : assets[type]).map((asset: Artifact) => {
    const { featured, publish_approved } = asset
    let description = asset.description || ""

    /* TODO make this less hackish */
    if (description) {
      description = description.split('. ')[0]
      description += description[description.length - 1] === '.' ? '' : '.'
    }

    return ({
      ...asset, type,
      description: description,
      featured: featured > 0,
      publish_approved: publish_approved > 0
    })
  })
  return assets
}

export async function fetchArtifactById(API: string, type: string, id: string) {
  if (!supported.includes(type))
    throw Error(`Can't fetch assets for type <${type}>. Unsupported.`)

  console.log(`fetching ${type} <id=${id}>`)

  const response = await fetch(`${API}/apis/v1alpha1/${type}/${id}`)
  return { ...(await response.json()), type }
}

export async function setFeaturedArtifacts(API: string, type: string, ids: string[]) {
  if (!supported.includes(type))
    throw Error(`Can't update asset of type <${type}>. Unsupported.`)

  console.log(`setting featured for artifact of <${type}> with id <${ids.toString()}>`)

  fetch(`${API}/apis/v1alpha1/${type}/featured`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(ids)
  })
}

export async function setPublishApprovedArtifacts(API: string, type: string, ids: string[]) {
  if (!supported.includes(type))
    throw Error(`Can't update asset of type <${type}>. Unsupported.`)

  fetch(`${API}/apis/v1alpha1/${type}/publish_approved`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(ids)
  })
}
