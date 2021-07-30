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
import React, { useContext, useState, ComponentProps, useEffect } from 'react'
import StoreContext from '../../lib/stores/context'
import { fetchArtifact } from '../../lib/api/artifacts';
import { Artifact, FETCH_ARTIFACT_ASSETS } from '../../lib/stores/artifacts'
import { SET_ACTIVE_PAGE } from '../../lib/stores/pages';
import { getUserInfo, hasRole, canShow } from '../../lib/util'
import fuzzysort from 'fuzzysort'

import Button from '../../components/Button'
import Hero from '../../components/Hero';
import Icon from '@material-ui/core/Icon'
import Link from '../../components/Link'
import MetaFeatured from './MetaFeatured';

import IconButton from "@material-ui/core/IconButton";
import InputAdornment from "@material-ui/core/InputAdornment";
import SearchIcon from "@material-ui/icons/Search";
import FormControl from '@material-ui/core/FormControl';
import Input from '@material-ui/core/Input';

import '../../styles/Models.css';
import { withStyles } from '@material-ui/core/styles';

const CssInput = withStyles({
  root: {
    '& label.Mui-focused': {
      color: 'green',
    },
    '& .MuiInput-underline:after': {
      borderBottomColor: 'green',
    },
    '& .MuiOutlinedInput-root': {
      '& fieldset': {
        borderColor: 'red',
      },
      '&:hover fieldset': {
        borderColor: 'yellow',
      },
      '&.Mui-focused fieldset': {
        borderColor: 'green',
      },
    },
  },
})(Input);


export interface MetaFeaturedPageProps extends ComponentProps<any> {
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

function MetaFeaturedPage(props: MetaFeaturedPageProps) {
  const {
    assetType, description, alternateBG: alternate,
    children, numFeatured,
    leftBtn, leftLink, leftIcon,
    rightBtn, rightLink, rightIcon,
    leftAdmin = false, rightAdmin = false,
  } = props

  const { store, dispatch } = useContext(StoreContext)
  const { artifacts, settings } = store
  const assets: Artifact[] = artifacts[assetType]
  const [search, setSearch] = useState('')

  let filteredAssets = assets
  const assetNames = assets.filter(asset => asset.featured && asset.publish_approved).map((asset: any) => asset.name)
  if (search !== '') {
    const searchResults = fuzzysort.go(search, assetNames)
    filteredAssets = searchResults.reduce(function(result, searchResult) {
      const index = assets.findIndex((asset: any) => asset.name === searchResult.target)
      if (index !== -1)
        result.push(assets[index])
      return result;
    }, []);
  }

  const API = settings.endpoints.api.value || settings.endpoints.api.default
  const upload = settings.capabilities.upload
  const canUpload = upload.value !== undefined ? upload.value : upload.default

  useEffect(() => {
    fetchArtifact(API, assetType)
      .then(assets => dispatch({
        type: FETCH_ARTIFACT_ASSETS,
        assetType,
        assets
      }))

    dispatch({
      type: SET_ACTIVE_PAGE,
      page: assetType
    })
  }, [API, assetType, dispatch])

  return (
    <div className="page-wrapper">
      <Hero
        title={assetType} 
        subtitle={description}
        alternate={alternate}
      >
        { assetType === "pipelines" && isAdmin &&
          <Link to='/experiments'>
            <Button
              className="hero-buttons-outline"
              variant="outlined"
              color="primary"
            >
              View Experiments
            </Button>
          </Link>
        }
        {leftBtn && leftLink && canShow(leftAdmin, isAdmin) &&
          <Link to={leftLink}>
            <Button
              className="hero-buttons"
              variant="contained"
              color="primary"
            >
              {leftIcon && <Icon>{leftIcon}</Icon>}
              {leftBtn}
            </Button>
          </Link>
        }
        <Link to="https://github.com/machine-learning-exchange/mlx">
          <Button
            className="hero-buttons"
            variant="contained"
            color="primary"
          >
            Github
          </Button>
        </Link>
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
        <FormControl className="search-box">
          <CssInput
            id="standard-adornment-weight"
            value={search}
            onChange={(event: React.ChangeEvent<HTMLInputElement>)=>setSearch(event.target.value)}
            placeholder="Search"
            endAdornment={
              <InputAdornment position="end">
                <IconButton>
                  <SearchIcon style={{fill: "#fff"}} />
                </IconButton>
              </InputAdornment>
            }
            inputProps={{
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton>
                    <SearchIcon />
                  </IconButton>
                </InputAdornment>
              )
            }}
          />
        </FormControl>
      </Hero>
        {children}
        {assets && 
          <MetaFeatured 
            numFeatured={numFeatured}
            assetType={assetType}
            assets={filteredAssets} 
          /> 
        }
    </div>
  );
}

export default MetaFeaturedPage
