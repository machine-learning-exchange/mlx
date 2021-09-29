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
import React from 'react'
import { withStyles, WithStyles } from '@material-ui/core'

import MetaCard from './MetaCard'

import Grid from '@material-ui/core/Grid'

interface MetaFeaturedProps extends WithStyles<typeof styles> {
  assets: any[]
  assetType: string
  numFeatured: number
}

const styles = {
  wrapper: {
    overflow: 'auto',
    padding: '0.8rem 0.6rem',
    flex: '1 0 auto'
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
  return (
    <div className={classes.wrapper}>
      <Grid container
        spacing={16}
        alignItems="flex-start"
        justify="flex-start"
        style={{ overflow: 'auto' }}
      >
        { assets.map(asset => {
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
      </Grid>
    </div>
  )
}

export default withStyles(styles)(MetaFeatured)
