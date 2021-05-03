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
import React, { useEffect, useState } from 'react'

import Button from '../components/Button/Button';
import Icon from '@material-ui/core/Icon'
import Link from '../components/Link';
import Hero from '../components/Hero';

interface IframePageProps {
  title: string,
  path: string,
  storageKey: string,
}

function IframePage(props: IframePageProps) {

  const [ iframeSrc, setIframeSrc ] = useState(props.path)

  // Checks if a url is held in local storage and loads the iframe from that url if so
  let iframeLoc = localStorage.getItem(props.storageKey)
  if (iframeLoc){
    setIframeSrc(iframeLoc)
    localStorage.removeItem(props.storageKey)
  }

  useEffect(() => {

    // Stores the url of the current page being displayed on iframe, so that if the user
    // refreshes the page we can reload the iframe at the url it was before the refresh
    onbeforeunload = (e: BeforeUnloadEvent) => {
      const element = document.getElementById("iframe") as HTMLIFrameElement
      try{
        localStorage.setItem(props.storageKey, element.contentDocument.URL)
      } catch(err) {
        // If this errors out because of the iframe being cross-origin then we just ignore
        // the error, this comes with the side effect of caching the iframe not working
        // However since current security practices do not allow you to access cross-origin 
        // iframe material caching the iframe's current location isn't possible.
      }
    }
  })

  return (

    <div className="page-wrapper">
      <Hero
      title={props.title} 
      subtitle={" "}
      alternate={true}
      >
        <Link to='/pipelines'>
          <Button
            className="hero-buttons-outline"
            variant="outlined"
            color="primary"
          >
            <Icon>{"arrow_back"}</Icon>
            Pipelines
          </Button>
        </Link>
        <Button
          className="hero-buttons"
          variant="contained"
          color="primary"
          onClick={() => {
              let elem = document.getElementById("iframe") as HTMLIFrameElement

              try {
                let url = elem.contentDocument.URL
                // Force refreshes the iframe if the current url is the same as the src
                if (url === iframeSrc)
                  elem.src = iframeSrc
                //  Changes the src if the current url is different than the src
                else
                  setIframeSrc(url)
                
              } catch(err) {
                // If this errors out because of the iframe being cross-origin then we just ignore
                // the error, this comes with the side effect of caching the iframe not working.
                // However since current security practices do not allow you to access cross-origin 
                // iframe material caching the iframe's current location isn't possible.

                // Force refreshes iframe by "changing" the src of the iframe
                elem.src = iframeSrc
              }
            }
          }
        >
          <Icon>refresh</Icon>
          Refresh
        </Button>
      </Hero>
      <iframe
        id="iframe"
        title={props.title}
        className="iframe-window"
        src={iframeSrc}
        height="100%"
      />
    </div>
  )
}

export default IframePage