/* 
* Copyright 2021 The MLX Contributors
* 
* SPDX-License-Identifier: Apache-2.0
*/ 
import React from 'react'
import { withStyles, WithStyles } from '@material-ui/core'

import Grid from '@material-ui/core/Grid'
import MetaCard from './KFServingCard'
import checkmark from '../../images/checkmark-outline.png'
import cancel from '../../images/cancel-outline.png'


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

function MetaFeatured(props: MetaFeaturedProps) {
  const { assets, classes } = props

  console.log("Asset:")
  console.log(props.assets)

  //return (<h1> Placeholder </h1>)

  return (
    <div className={classes.wrapper}>
      <Grid container
        spacing={16}
        alignItems="flex-start"
        justify="flex-start"
        style={{ overflow: 'auto' }}
      >
        {assets.map(asset => {
          const name = asset.metadata.name;
          
          let runningStatus = ""
          let statusIcon = ""
          if (asset.status.conditions) {
            runningStatus = asset.status?.conditions[0]?.status || ""

            if (asset.status) {
              for (var i=0; i< asset.status.conditions.length; i++) {
                if (asset.status.conditions[i].type === "Ready") {
                  const index = asset.status.conditions.indexOf(asset.status.conditions[i])
                  runningStatus = asset.status.conditions[index].status
                  if (runningStatus === 'True') {
                    statusIcon = checkmark
                  }
                  else {
                    statusIcon = cancel
                  }
                }
              }
            }
          }
          else {
            runningStatus = asset.status.available
            if (runningStatus === 'true')
              statusIcon = checkmark
            else
              statusIcon = cancel
          }
          const description = asset.kind;
          const tag = Object.keys(asset.spec).join(",")
          const link = "inferenceservices"
          let predictor = asset.spec.predictor
          let framework = ""
          if (asset.spec.predictor) {
            framework = predictor.tensorflow ? "tensorflow" 
                              : predictor.keras ? "keras"
                              : predictor.sklearn ? "sklearn"
                              : predictor["scikit-learn"] ? "sklearn"
                              : predictor.pytorch ? "pytorch" : "custom"
          }
          else {
            framework = asset.spec.modelType.name
          }
          return (
            <Grid item key={name} xs md={4}
             lg={3} xl={2} className={classes.card} >
              <MetaCard
                name={name}
                runningStatus={runningStatus}
                statusIcon={statusIcon}
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
