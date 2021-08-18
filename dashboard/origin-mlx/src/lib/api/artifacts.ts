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
import yaml from 'js-yaml'

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

interface cacheEntry {
  response: any,
  time: number
}

// Time to live references the lifespan of elements in the cache
const timeToLive = process.env.REACT_APP_TTL ?  Number(process.env.REACT_APP_TTL) : 24 * 60 * 60
// Cache check interval is the minimum time between checks on the validity of cache entries
const cacheCheckInterval = process.env.REACT_APP_CACHE_INTERVAL ? Number(process.env.REACT_APP_CACHE_INTERVAL) : 24 * 60 * 60

export async function resetCache() {
  Object.keys(localStorage).forEach((key: string) => {
    if (key.substring(0,9) === "mlx-cache") {
      localStorage.removeItem(key)
    }
  })
}

// Remove any cache entries older than the time to live
export async function findInvalidCacheEntries() {
  const lastCheck = localStorage.getItem("mlx-last-invalid-cache-check")
  const currentDate = Date.now()
  // If there is no time stamp or the time stamp is older than the time to live then check 
  // for invalid entries. Division by 1000 is due to Date counting in milliseconds.
  if (!lastCheck || (currentDate - Number(lastCheck)) / 1000 > cacheCheckInterval) {
    localStorage.setItem("mlx-last-invalid-cache-check", "" + currentDate)
    Object.keys(localStorage).forEach((key: string) => {
      if (key.substring(0,9) === "mlx-cache" && (currentDate - Number(JSON.parse(localStorage.getItem(key)).time)) / 1000 > timeToLive) {
        localStorage.removeItem(key)
      }
    })
  }
}

async function sendRequestApi(request: string) {
  return (await fetch(request)).json()
}

// Pull response from cache if available otherwise send api request
async function sendRequest(request: string) {
  const cacheKey = `mlx-cache-${request}`
  const cachedRequest = localStorage.getItem(cacheKey)
  // If a cache entry exists and it is still valid return that, otherwise make an API call
  if (cachedRequest && (Date.now() - Number(JSON.parse(cachedRequest).time)) / 1000 < timeToLive) {
    return Promise.resolve(JSON.parse(cachedRequest).response)
  }
  else {
    const template : cacheEntry = {response: await sendRequestApi(request), time: Date.now()}
    localStorage.setItem(cacheKey, JSON.stringify(template))
    return Promise.resolve(template.response)
  }
}

export async function fetchArtifact(API: string, type: string, namespace?: string) {
  if (!supported.includes(type) && !mocked.includes(type))
    throw Error(`Can't fetch assets for type <${type}>. Unsupported.`)

  const request = type === "inferenceservices"
    ? `${API}/apis/v1alpha1/${type}${namespace ? `?namespace=${namespace}` : ''}`
    : `${API}/apis/v1alpha1/${type}`
  const response = await sendRequestApi(request)
  let assets = response

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

export async function fetchAssetById(API: string, type: string, id: string) {
  if (!supported.includes(type))
    throw Error(`Can't fetch assets for type <${type}>. Unsupported.`)

  console.log(`fetching ${type} <id=${id}>`)

  const request = `${API}/apis/v1alpha1/${type}/${id}`
  return sendRequest(request)
}

export async function fetchAssetTemplates(API: string, type: string, asset: any) {
  const request = `${API}/apis/v1alpha1/${type}/${asset.id}/templates`
  const data = await sendRequest(request)

  const typesWithMultipleTemplates = [ 'operators' ]

  if (Array.isArray(data)) {
    if (!typesWithMultipleTemplates.includes(type))
      throw Error(`Received multiple templates for <${type}>. Expected one.`)
    
    return ({
      ...asset,
      templates: Object.fromEntries(await Promise.all(data.map(({ template: raw, url }: any) => {
        const template = yaml.load(raw);
        return [ template.kind || 'Definition', { raw, template, url } ]
      }, data)))
    })
  }

  return ({
    ...asset,
    yaml: data.template,
    template: yaml.safeLoad(data.template)
  })
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
