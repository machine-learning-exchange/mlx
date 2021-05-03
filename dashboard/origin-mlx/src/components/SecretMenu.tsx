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
import React, { useContext } from 'react'
import StoreContext from '../lib/stores/context'
import { Typography } from '@material-ui/core';
import { Link } from 'react-router-dom';


export default function SecretMenu () {
  const { settings } = useContext(StoreContext).store
  const { branding, endpoints } = settings

  const API = endpoints.api.value || endpoints.api.default
  const KFP = endpoints.kfp.value || endpoints.kfp.default

  const shortenBrand = (brand: string) => {
    if (brand.length <= 10)
      return brand;

    const split = brand.split(' ')
    let brandAbrev = ""
    split.forEach((word: string) => {
      if (word.toLowerCase() === "exchange")
        brandAbrev += "X"
      else
       brandAbrev += word[0].toUpperCase()
    })
    return brandAbrev
  }

  return (
    <div className="secret-menu visible">
      <Typography className="secret-heading" variant="subtitle2">
        [x] click panel to close
      </Typography>
      <ul>
        <li>
          <Link to="/settings">
            {`${shortenBrand(branding.name.value || branding.name.default)} Settings`}
          </Link>
        </li>
        <li>
          <a target="_blank" rel="noopener noreferrer" href={`${API}/apis/v1alpha1/ui`}>
            API Swagger Docs
          </a>
        </li>
        <li>
          <a target="_blank" rel="noopener noreferrer" href={`${KFP}/pipeline/#`}>
            Pipeline Backend
          </a>
        </li>
        <li>
          <a target="_blank" rel="noopener noreferrer" href={`${KFP}`}>
            Kubeflow Dashboard
          </a>
        </li>
      </ul>
    </div>
  );
}
