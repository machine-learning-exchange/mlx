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
import React, { useState } from 'react'
import { withStyles, WithStyles } from '@material-ui/core'
import fuzzysort from 'fuzzysort'

import MetaCard from './MetaCard'
import PageFooter from '../../components/PageFooter';

import Grid from '@material-ui/core/Grid'
import IconButton from "@material-ui/core/IconButton";
import InputAdornment from "@material-ui/core/InputAdornment";
import SearchIcon from "@material-ui/icons/Search";
import FormControl from '@material-ui/core/FormControl';
import Input from '@material-ui/core/Input';

interface MetaFeaturedProps extends WithStyles<typeof styles> {
  assets: any[]
  assetType: string
  numFeatured: number
}

const styles = {
  wrapper: {
    overflow: 'auto',
    padding: '0.8rem 0.6rem'
  },
  card: {
    // width: '20%'
    // maxWidth: '275px'
  }
}

const getDetails = (asset: any, type: string) => {
  switch (type) {
    case 'pipelines':
      return {
        tag: asset.metadata?.annotations?.category
          || 'OpenSource',
        link: '/pipelines'
      }
    case 'datasets':
      return {
        tag: asset.metadata?.annotations?.category
          || 'OpenSource',
        link: '/datasets'
      }
    case 'components':
      return {
        tag: asset.metadata?.annotations?.platform
          || 'OpenSource',
        link: '/components'
      }
    case 'models':
      return {
        tag: asset.domain,
        link: '/models',
        framework: asset.framework.name
      }
    case 'operators':
      return {
        tag: asset.metadata.annotations.categories,
        link: '/operators'
      }
    case 'notebooks':
      return {
        tag: asset.metadata.annotations.platform,
        title: asset.name,
        link: '/notebooks'
      }
  }
}

function MetaFeatured(props: MetaFeaturedProps) {
  const { assets, assetType, classes } = props
  const assetNames = assets.map((asset: any) => asset.name)
  const [search, setSearch] = useState('')
  let filteredAssets = assets
  if (search !== '') {
    const searchResults = fuzzysort.go(search, assetNames)
    filteredAssets =  searchResults.reduce(function(result, searchResult) {
      const index = assets.findIndex((asset: any) => asset.name === searchResult.target)
      if (index !== -1)
        result.push(assets[index])
      return result;
    }, []);
  }

  return (
    <div className={classes.wrapper}>
      <FormControl className="search-box">
        <Input
          id="standard-adornment-weight"
          value={search}
          onChange={(event: React.ChangeEvent<HTMLInputElement>)=>setSearch(event.target.value)}
          placeholder="Search"
          endAdornment={
            <InputAdornment position="end">
              <IconButton>
                <SearchIcon />
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
      <Grid container
        spacing={16}
        alignItems="flex-start"
        justify="flex-start"
        style={{ overflow: 'auto' }}
      >
        { filteredAssets.map(asset => {
          const { name, description } = asset
          const { tag, link, framework } = getDetails(asset, assetType);
          return (
            <Grid item key={name} xs md={4}
             lg={3} xl={2} className={classes.card} >
              <MetaCard
                name={name}
                description={description}
                link={link}
                tag={tag}
                framework={framework}
                asset={asset}
              />
            </Grid>
          )
        })}
        <PageFooter/>
      </Grid>
    </div>
  )
}

export default withStyles(styles)(MetaFeatured)
