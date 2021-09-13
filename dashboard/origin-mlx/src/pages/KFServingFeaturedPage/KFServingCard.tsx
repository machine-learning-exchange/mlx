/* 
* Copyright 2021 IBM Corporation
* 
* SPDX-License-Identifier: Apache-2.0
*/ 
import React from 'react'
import { withStyles, WithStyles } from '@material-ui/core/styles';

import Card from '@material-ui/core/Card'
import CardHeader from '@material-ui/core/CardHeader'
import CardContent from '@material-ui/core/CardContent';
import Chip from '@material-ui/core/Chip';
import Grid from '@material-ui/core/Grid'
import { Link } from 'react-router-dom'

import tfLogo from '../../images/tf-logo.png'
import kerasLogo from '../../images/keras-logo.png'
import pytorchLogo from '../../images/pytorch-logo.png'
import sklearnLogo from '../../images/scikit-learn-logo.png'
import kubeflowLogo from '../../images/kubeflow-logo.png'


interface KFServingCardProps extends WithStyles<typeof styles>{
  name: string
  runningStatus: string
  statusIcon: string
  description: string
  link: string
  tag: string
  framework?: string
  id?: string
  asset?: any
  pipeLink?: string
}

const styles = {
  card: {
    minWidth: '250px',
    // maxWidth: '275px',
    height: '275px',
    backgroundColor: '#525252',
    borderRadius: '7px'
  },
  container: {
    height: 'inherit',
    padding: '8px'
  },
  wrap: {
    padding: '0px !important'
  },
  header: {
    color: '#1ccdc7',
    fontSize: '1.3rem',
    fontWeight: 500
  },
  description: {
    color: 'white !important',
    fontSize: '0.9rem',
    overflow: 'auto'
  },
  chip: {
    margin: '3px',
    color: '#ccc',
    border: '1px solid #ccc'
  }
}

function KFServingCard(props: KFServingCardProps) {
  const { name, statusIcon, link, tag, framework, asset, classes } = props
  
  let tags = tag ? 
                tag.includes(',') ? tag.split(',') : [tag]
                : [""]
  tags = tags.filter(function( element ) {
    return element !== 'undefined';
  });
  const logo = getLogo(framework)

  return (
    <Link to={{
      pathname: `${link}/${name}`,
      state: asset
    }}>
      <Card className={classes.card} >
        <Grid container
          direction="column"
          justify="space-between"
          className={classes.container}
        >
          <Grid item>
            <div style={{display: 'flex', flexDirection: 'row'}}>
              <CardHeader title={name.replace(/(^|-)[a-z]/g, (a) => {return (a[1] ? ' ' + a[1] : a[0]).toUpperCase();})}
                titleTypographyProps={{
                  variant: 'h6',
                  component: 'h2',
                  className: classes.header
                }}
                className={classes.wrap}
              />
              
            </div>

            {/* <Divider /> */}
            <div className="divider" />
            <CardContent className={classes.wrap}>
              <div style={{display: 'flex', flexDirection: 'row'}}>
                <div style={{fontSize: '14px', color: 'white', marginTop: '8px'}}>Status: </div>
                <img style={{marginLeft: '10px', marginTop: '10px'}} src={statusIcon} alt={statusIcon} height="15"/>
              </div>
              </CardContent>
          </Grid>
          <Grid item>
            <Grid container justify="space-between">
              <Grid item>
                <CardContent className={classes.wrap}>
                  {tags.map(tag =>
                    <Chip key={tag} label={tag} variant="outlined" className={classes.chip} />)}
                </CardContent>
              </Grid>
              {logo &&
                <Grid item>
                  <CardContent className={classes.wrap}>
                    <img src={logo} alt={logo} height="40"/>
                  </CardContent>
                </Grid>}
            </Grid>
          </Grid>
        </Grid>
      </Card>
    </Link>
  )
}

function getLogo(framework: string) {
  switch (framework) {
    case 'pytorch':
      return pytorchLogo
    case 'tensorflow':
      return tfLogo
    case 'keras':
      return kerasLogo
    case 'sklearn' || 'scikit-learn':
      return sklearnLogo
    default:
      return kubeflowLogo
  }
}

export default withStyles(styles)(KFServingCard)
