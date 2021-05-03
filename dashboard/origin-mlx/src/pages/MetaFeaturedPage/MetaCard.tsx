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
import { withStyles, WithStyles } from '@material-ui/core/styles';

import Card from '@material-ui/core/Card'
import CardHeader from '@material-ui/core/CardHeader'
import CardContent from '@material-ui/core/CardContent';
import Chip from '@material-ui/core/Chip';
import Grid from '@material-ui/core/Grid'
import { Link } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import Typography from '@material-ui/core/Typography'

import tfLogo from '../../images/tf-logo.png'
import kerasLogo from '../../images/keras-logo.png'
import pytorchLogo from '../../images/pytorch-logo.png'
import sklearnLogo from '../../images/scikit-learn-logo.png'
import { firstSentence } from '../../lib/util';


interface MetaCardProps extends WithStyles<typeof styles>{
  name: string
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

function MetaCard(props: MetaCardProps) {
  const { name, link, tag, framework, asset, classes } = props

  const description = firstSentence(props.description || 'Component for your Pipelines.')

  const tags = tag.includes(',') ? tag.split(',') : [tag]
  const logo = getLogo(framework)

  return (
    <Link to={{
      pathname: `${link}/${asset.id}`,
      state: asset
    }}>
      <Card className={classes.card} >
        <Grid container
          direction="column"
          justify="space-between"
          className={classes.container}
        >
          <Grid item>
            <CardHeader title={name}
              titleTypographyProps={{
                variant: 'h6',
                component: 'h2',
                className: classes.header
              }}
              className={classes.wrap}
            />
            {/* <Divider /> */}
            <div className="divider" />
            <CardContent className={classes.wrap}>
              <ReactMarkdown
                source={description} renderers={{
                  paragraph: ({children}) =>
                    <Typography
                      variant="body1"
                      component="p"
                      className={classes.description}
                    >
                      {children}
                    </Typography>, 
                  link: ({children}) => children
                }}
              />
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
      return null
  }
}


export default withStyles(styles)(MetaCard)
