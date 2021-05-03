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
import React, { useContext, useEffect, useState, Children, ReactNode, ReactElement } from 'react'
import { capitalize } from '../lib/util';
import StoreContext from '../lib/stores/context'
import yaml from 'js-yaml'

import Button from '../components/Button/Button';
import Icon from '@material-ui/core/Icon'
import Hero from '../components/Hero';
import Link from '../components/Link';
import LoadingMessage from '../components/LoadingMessage';

interface MetaDetailPageProps {
  children: ReactNode,
  type: string,
  id: string,
  asset?: any
}

async function fetchAssetTemplates(API: string, type: string, asset: any) {
  const res = await fetch(`${API}/apis/v1alpha1/${type}/${asset.metadata.name}`)
  const data = await res.json()

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
    yaml: data.template || '',
    template: yaml.safeLoad(data.template) || ''
  })
}

async function fetchAssetById(API: string, type: string, id: string) {
  return (await fetch(`${API}/apis/v1alpha1/${type}/${id}`)).json()
}

function MetaDetailPage(props: MetaDetailPageProps) {
  const { children, type, id } = props
  const [ asset, setAsset ] = useState(props.asset.state)

  const { store } = useContext(StoreContext)
  const { api } = store.settings.endpoints
  const namespace = store.settings.kfserving.namespace.value || store.settings.kfserving.namespace.default
  const API = api.value || api.default

  useEffect(() => {
    if (!asset?.template && !asset?.templates) {
      (asset ? Promise.resolve(asset) : fetchAssetById(API, type, id))
        .then(asset => fetchAssetTemplates(API, type, asset))
        .then((template: any) => {
          if (props.asset.search) {
            const url_params = props.asset.search.substring(1).split("&")
            const url_params_json: {[key: string]: string} = {}
            url_params.forEach((param: string) => {
              const split = param.split("=")
              if (type === "pipelines")
                url_params_json[split[0].replace(/_/g,"-")] = split[1]
              else
                url_params_json[split[0]] = split[1]
            })
            template.url_parameters = url_params_json
          }
          else
            template.url_parameters = {}
          setAsset(template)
        })
    }
  }, [API, asset, id, props.asset.search, type])

  const child = Children.only(children) as ReactElement

  return (
    <div className="page-wrapper">
      <Hero
        title={asset?.name || id}
          subtitle={' '}
        // subtitle={asset
        //   ? asset.description.split[0] + '.'
        //   : `Now loading your wonderful ${type}.`}
      >
        <Link to={`/${type}`}>
          <Button
            className="hero-buttons-outline"
            variant="outlined"
            color="primary"
          >
            <Icon>arrow_back</Icon>
            {capitalize(type)}
          </Button>
        </Link>
      </Hero>
      { 
        asset && (asset.template || asset.templates)
          ? <div className="detail-body-wrapper"> {React.cloneElement(child, { namespace, type, id, ...child.props, asset, })} </div>
          : <LoadingMessage assetType={type} />           
      }
    </div>
  )
}

export default MetaDetailPage
