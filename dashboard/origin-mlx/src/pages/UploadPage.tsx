/* 
* Copyright 2021 IBM Corporation 
* 
* SPDX-License-Identifier: Apache-2.0
*/ 
import React, { useContext, useState, ChangeEvent, FormEvent } from 'react'
import StoreContext from '../lib/stores/context'
import { Link } from 'react-router-dom'
import { RouteComponentProps } from 'react-router';
import { capitalize } from '../lib/util'
import { upload, uploadFromUrl } from '../lib/api/upload'
import PageFooter from '../components/PageFooter';

import Button from '../components/Button'
import Icon from '@material-ui/core/Icon'
import Hero from '../components/Hero'
import Paper from '@material-ui/core/Paper'
import TextField from '@material-ui/core/TextField'
import Typography from '@material-ui/core/Typography'

import { UPDATE_ARTIFACT_ASSET } from '../lib/stores/artifacts'
import { Artifact } from '../lib/stores/artifacts'
import { setFeaturedArtifacts, setPublishApprovedArtifacts } from '../lib/api/artifacts';


interface MatchProps {
  type: string
}

function UploadPage(props: RouteComponentProps<MatchProps>) {
  const { type } = props.match.params
  const [ name, setName ] = useState('')
  const [ url, setUrl ] = useState('')
  const [ enterpriseToken, setEnterpriseToken ] = useState('')
  const [ uploadStatus, setUploadStatus] = useState({fullStatus: '', link: ''})
  const [ file, setFile ] = useState(null)
  const [ loading, setLoading ] = useState(false)
  const [ error, setError ] = useState('')

  const { store, dispatch } = useContext(StoreContext)
  const { artifacts, settings } = store
  const API = settings.endpoints.api.value || settings.endpoints.api.default
  const singularType = type.substring(0, type.length - 1)

  const assets: {[key: string]: Artifact} = Object.fromEntries(artifacts[type]
    .map((asset: Artifact) => [asset.name, asset]))

  const featured = new Set(Object.entries(assets)
    .filter(([_, asset]) => asset.featured)
    .map(([_, asset]) => asset.id))

  const publishable = new Set(Object.entries(assets)
    .filter(([_, asset]) => asset.publish_approved)
    .map(([_, asset]) => asset.id))

  const handleFile = (e: ChangeEvent<HTMLInputElement>) => {
    setFile(e.currentTarget.files[0])
    setError('')
    setUploadStatus({fullStatus: e.currentTarget.files[0].name, link: ''})
  }

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    if (file || url) {
      setLoading(true)
      let response;
      if (file) {
        response = await upload(API, type, file, {
          name, url, token: enterpriseToken
        })
      }
      else {
        response = await uploadFromUrl(API, type, url, {
          name, url, token: enterpriseToken
        })
      }
      setLoading(false)

      if (response.status < 200 || response.status >= 300)
        response.text().then(text => {
          setError(text)
          setUploadStatus({fullStatus: ("Upload of " + file.name + " failed"), link: ''})
        })
      else{
        const response_json = await response.json()

        // Makes the newly uploaded file publishable and featured
        const path = response_json.id
        setUploadStatus({fullStatus: ("Upload Suceeded. Click to view "), link: path})

        publishable.add(path)
        featured.add(path)

        await setPublishApprovedArtifacts(API, type, Array.from(publishable.values()))
          .then(() => dispatch({
            type: UPDATE_ARTIFACT_ASSET, assetType: type,
            path, payload: { publish_approved: true }
          }))

        await setFeaturedArtifacts(API, type, Array.from(featured.values()))
          .then(() => dispatch({
            type: UPDATE_ARTIFACT_ASSET, assetType: type,
            path, payload: { featured: true }
          }))
      }

      setFile(null)
      setUrl("")
    }
  }

  return (
    <div className="page-wrapper">
      <Hero
        title={type} 
        subtitle={`Register a ${type.substring(0, type.length - 1)}`}
      >
        <Link to={`/${type}`}>
          <Button
            className="hero-buttons-outline"
            variant="outlined"
            color="primary"
          >
            <Icon>arrow_back</Icon>
            Featured
          </Button>
        </Link>
        <Link to="https://github.com/machine-learning-exchange/mlx">
          <Button
            className="hero-buttons-outline"
            variant="outlined"
            color="primary"
          >
            Github
          </Button>
        </Link>
      </Hero>
      <div className="upload-wrapper">
        <Paper className="upload-form-wrapper">
          <Typography variant="title" className="upload-heading">
            Enter a name for your new {singularType}.
          </Typography>
          <form
            method="post" 
            encType="multipart/form-data"
            onSubmit={handleSubmit}
          >
            <TextField
              value={name}
              onChange={(e: ChangeEvent<HTMLInputElement>) => setName(e.currentTarget.value)}
              fullWidth
              margin="dense"
              variant="outlined"
              autoCorrect="false"
              label={`${capitalize(singularType)} Name`}
              helperText={`The ${singularType} name should be in title case without periods (.), dashes (-), or underscores (_).`}
              InputLabelProps={{ shrink: true }}
            />
            <div style={{ margin: '0.5rem 0' }} />
            {type === 'notebooks' &&
              <TextField
                value={enterpriseToken}
                onChange={(e: ChangeEvent<HTMLInputElement>) => setEnterpriseToken(e.currentTarget.value)}
                fullWidth
                margin="dense"
                variant="outlined"
                autoCorrect="false"
                label={`${capitalize(type)} Enterprise GitHub Token (if necessary)`}
                helperText="If no value is entered, and a token is necessary, your upload may fail."
                InputLabelProps={{
                  shrink: true,
                }}
              />
            }
            <Typography variant="title" className="upload-heading">
              Select a <code>.tgz</code>, <code>.tar.gz</code>, <code>.yaml</code>, or <code>.yml</code> file or enter a github url to register a new {type.substring(0, type.length - 1)}.
            </Typography>
            <div className="filePicker-wrapper">
              <input 
                type="file" 
                onChange={handleFile}
                accept=".tgz, .gz, .yaml, .yml"
              />
            </div>
          </form>
          <Typography variant="title" className="upload-heading">
            Alternatively, use a github url to register a new {type.substring(0, type.length - 1)}.
          </Typography>
          <TextField
            value={url}
            onChange={(e: ChangeEvent<HTMLInputElement>) => setUrl(e.currentTarget.value)}
            fullWidth
            margin="dense"
            variant="outlined"
            autoCorrect="false"
            label={`${capitalize(singularType)} GitHub URL`}
            helperText={`A Github URL to a ${singularType} asset.`}
            InputLabelProps={{ shrink: true }}
          />
          <div className="upload-button-wrapper">
            <Button 
              className="hero-buttons upload-button" 
              variant="contained" 
              color="primary"
              type="submit"
              onClick={handleSubmit}
            >
              <Icon>cloud_upload</Icon>
              {`Upload`}
            </Button>
          </div>
          {error && 
            <p className="error-msg">
              {`Upload Error: Please Retry - ${error}`}
            </p>
          }
          {loading &&
            <p className="upload-msg">
              {`Uploading...`}
            </p>
          }
          { uploadStatus.link &&
            <Link to={`/${type}/${uploadStatus.link}`}>
              <p className="selected-file">{uploadStatus.fullStatus}</p>
            </Link>
          }
        </Paper>
      </div>
      <PageFooter/>
    </div>
  )
}

export default UploadPage
