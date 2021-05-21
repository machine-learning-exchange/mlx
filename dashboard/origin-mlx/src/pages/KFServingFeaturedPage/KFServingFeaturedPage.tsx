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
import React, { useContext, ComponentProps, useEffect } from 'react'
import StoreContext from '../../lib/stores/context'
import { fetchArtifact } from '../../lib/api/artifacts';
import { Artifact, FETCH_ARTIFACT_ASSETS } from '../../lib/stores/artifacts'
import { SET_ACTIVE_PAGE } from '../../lib/stores/pages';
import { getUserInfo, hasRole, canShow  } from '../../lib/util';

import Button from '../../components/Button'
import Hero from '../../components/Hero';
import Icon from '@material-ui/core/Icon'
import Link from '../../components/Link'
import MetaFeatured from './KFServingFeatured';
import '../../styles/Models.css';


export interface KFServingFeaturedPageProps extends ComponentProps<any> {
  assetType: string;
  description: string;
  alternateBG?: boolean;
  leftBtn?: string;
  leftLink?: string;
  leftIcon?: string;
  leftAdmin?: boolean;
  rightBtn?: string;
  rightLink?: string;
  rightIcon?: string;
  rightAdmin?: boolean;
}

const isAdmin = hasRole(getUserInfo(), 'admin');

function KFServingFeaturedPage(props: KFServingFeaturedPageProps) {
  var {
    assetType, description, alternateBG: alternate,
    children, numFeatured,
    leftBtn, leftLink, leftIcon,
    rightBtn, rightLink, rightIcon,
    rightAdmin = false, leftAdmin = false,
  } = props

  const { store, dispatch } = useContext(StoreContext)
  const { artifacts, settings } = store
  const assets: Artifact[] = artifacts[assetType]

  // console.log(assets)

  const API = settings.endpoints.api.value || settings.endpoints.api.default
  const upload = settings.capabilities.upload
  const canUpload = upload.value !== undefined ? upload.value : upload.default
  const namespace = settings.kfserving.namespace.value || settings.kfserving.namespace.default

  useEffect(() => {
    fetchArtifact(API, assetType, namespace)
      .then(assets => dispatch({
        type: FETCH_ARTIFACT_ASSETS,
        assetType,
        assets
      }))

    dispatch({
      type: SET_ACTIVE_PAGE,
      page: assetType
    })
  }, [API, namespace, assetType, dispatch])

  return (
    <div className="page-wrapper">
      <Hero
        title='KFServices'
        subtitle={description}
        alternate={alternate}
      >
        { assetType === "pipelines" &&
          <Link to='/experiments'>
            <Button
              className="hero-buttons"
              variant="contained"
              color="primary"
            >
              View Experiments
            </Button>
          </Link>
        }
        {leftBtn && leftLink && canShow(leftAdmin, isAdmin) &&
          <Link to={leftLink}>
            <Button
              className="hero-buttons-outline"
              variant="outlined"
              color="primary"
            >
              {leftIcon && <Icon>{leftIcon}</Icon>}
              {leftBtn}
            </Button>
          </Link>
        }
        {rightBtn && rightLink && canUpload && canShow(rightAdmin, isAdmin) &&
          <Link to={rightLink}>
            <Button
              className="hero-buttons"
              variant="contained"
              color="primary"
            >
              {rightIcon && <Icon>{rightIcon}</Icon>}
              {rightBtn}
            </Button>
          </Link>
        }
        { (assetType === "components" || assetType === "notebooks") &&
          <Link to='/pipelines/creator'>
            <Button
              className="hero-buttons-outline"
              variant="outlined"
              color="primary"
            >
              {leftIcon && <Icon>{leftIcon}</Icon>}
              Pipeline Creator
            </Button>
          </Link>
        }
      </Hero>
        {children}
        {assets && 
          <MetaFeatured 
            numFeatured={numFeatured}
            assetType={assetType}
            assets={assets} 
          /> 
        }
    </div>
  );
}

export default KFServingFeaturedPage
