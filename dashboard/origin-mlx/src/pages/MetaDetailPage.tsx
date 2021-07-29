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
import { capitalize, formatTitle } from '../lib/util';
import StoreContext from '../lib/stores/context'

import Button from '../components/Button/Button';
import ButtonWithTooltip from '../components/Button/ButtonWithTooltip';
import Icon from '@material-ui/core/Icon'
import Hero from '../components/Hero';
import Link from '../components/Link';
import LoadingMessage from '../components/LoadingMessage';
import PageFooter from '../components/PageFooter';
import { fetchAssetById, fetchAssetTemplates } from '../lib/api/artifacts';

interface MetaDetailPageProps {
  children: ReactNode,
  type: string,
  id: string,
  asset?: any
}

function MetaDetailPage(props: MetaDetailPageProps) {
  const { children, type, id } = props
  const [ asset, setAsset ] = useState(props.asset.state)
  const [ runLink, setRunLink ] = useState("")
  const [ isLoading, setIsLoading ] = useState(false)

  const { store } = useContext(StoreContext)
  const { api } = store.settings.endpoints
  const API = api.value || api.default

  const fetchTemplates = () => {
    fetchAssetTemplates(API, type, asset)
    .then((template: any) => {
      if (props.asset.search) {
        const url_params = props.asset.search.substring(1).split("&")
        const url_params_json: {[key: string]: string} = {}
        url_params.forEach((param: string) => {
          const split = decodeURIComponent(param).split("=")
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
    setIsLoading(false)
  }

  useEffect(() => {
    if (!asset?.template && !asset?.templates) {
      setIsLoading(true)
      if (!asset)
        fetchAssetById(API, type, id)
        .then((asset: any) => {
          setAsset(asset)
        })
        .catch((error) => {
          console.error('Error fetching asset: ', error);
        });
      else {
        fetchTemplates()
      }
    }
  }, [API, asset, id, props.asset.search, type])

  const child = Children.only(children) as ReactElement

  return (
    <div className="page-wrapper">
      <Hero
        title={formatTitle(asset ? asset.name || "" : type)}
        subtitle={asset && asset.description
          ? asset.description.split('.')[0] + '.'
          : `Now loading your wonderful ${type}.`}
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
        { runLink && 
          <Button
            className="hero-buttons-outline"
            variant="outlined"
            color="primary"
            onClick={() => {
              let elem = document.getElementById("iframe-run") as HTMLIFrameElement
              try {
                let url = elem.contentDocument.URL
                // Force refreshes the iframe if the current url is the same as the src
                if (url === runLink)
                  elem.src = runLink
                //  Changes the src if the current url is different than the src
                else
                  setRunLink(url)

              } catch(err) {
                // If this errors out because of the iframe being cross-origin then we just ignore
                // the error, this comes with the side effect of caching the iframe not working.
                // However since current security practices do not allow you to access cross-origin 
                // iframe material caching the iframe's current location isn't possible.

                // Force refreshes iframe by "changing" the src of the iframe
                elem.src = runLink
              }
            }}
          >
            <Icon>refresh</Icon>
            Refresh
          </Button>
        }
        <ButtonWithTooltip
          className="hero-buttons"
          variant="contained"
          color="primary"
          tooltip={`Metadata YAML and sample pipeline`}
          onClick={(event: never) =>
            window.open(`${API}/apis/v1alpha1/${type}/${asset.id}`
              + '/download?include_generated_code=true', '_blank')}
        >
          <Icon>cloud_download</Icon>
          Download
        </ButtonWithTooltip>
      </Hero>
      { !runLink ?
        asset && (asset.template || asset.templates)
          ? <div className="body-wrapper"> {React.cloneElement(child, { API, type, id, ...child.props, asset, setRunLink})} </div>
          : isLoading 
            ? <LoadingMessage assetType={type} />
            : <h1> Asset not found </h1>
        : <iframe
            id="iframe-run"
            title="Kubeflow Pipelines Experiment Run"
            className="iframe-window"
            src={runLink}
            height="100%"
          />
      }
      <PageFooter/>
    </div>
  )
}

export default MetaDetailPage
