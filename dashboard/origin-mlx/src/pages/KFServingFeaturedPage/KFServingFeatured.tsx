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

  // console.log(assets)
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
          var runningStatus = asset.status?.conditions[0]?.status || ""
          var statusIcon = ""

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
          
          const description = asset.kind;
          const tag = Object.keys(asset.spec.default)[0] + ',' + Object.keys(asset.spec.default)[1]
          const link = "inferenceservices"
          const predictor = asset.spec.default.predictor
          const framework = predictor.tensorflow ? "tensorflow" 
                            : predictor.keras ? "keras"
                            : predictor.sklearn ? "sklearn"
                            : predictor["scikit-learn"] ? "sklearn"
                            : predictor.pytorch ? "pytorch" : "custom"
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
