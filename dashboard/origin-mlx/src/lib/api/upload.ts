// Copyright 2021 IBM Corporation
// 
// SPDX-License-Identifier: Apache-2.0

const supportedTypes = [
  'pipelines',
  'datasets',
  'components',
  'models',
  'notebooks',
  'inferenceservices'
]

interface UploadOptionals {
  name?: string
  url?: string
  token?: string
}

export async function upload(
  API: string,
  type: string,
  file: File,
  options: UploadOptionals
) {
  if (!supportedTypes.includes(type))
    throw Error(`Upload for <${type}> components is not supported`)

  const { name, url, token } = options

  const data = new FormData()
  data.append('uploadfile', file)
  data.append('enterprise_github_token', token)

  const endpoint = `/${type}/upload?` + (name ? `name=${name}` : ``) + (url ? `&url=${url}` : ``)
  return await fetch(`${API}/apis/v1alpha1${endpoint}`, {
    method: 'POST',
    body: data
  })
}

export async function uploadFromUrl(
  API: string,
  type: string,
  githubUrl: string,
  options: UploadOptionals
) {
  if (!supportedTypes.includes(type))
    throw Error(`Upload for <${type}> components is not supported`)

  const { name, url, token } = options

  const data = new FormData()
  data.append('url', githubUrl)
  data.append('enterprise_github_token', token)

  const endpoint = `/${type}/upload_from_url?` + (name && `name=${name}`) + (url && `&url=${url}`)
  return await fetch(`${API}/apis/v1alpha1${endpoint}`, {
    method: 'POST',
    body: data
  })
}

export async function importCatalog(
  API: string,
  body: any
) {

  return await fetch(`${API}/apis/v1alpha1/catalog`, {
    headers: {
      'Content-type': 'application/json'
    },
    method: 'POST',
    body: body
  })
}