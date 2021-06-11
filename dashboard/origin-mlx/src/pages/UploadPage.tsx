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
import React, { useContext, useState, ChangeEvent, FormEvent } from 'react'
import StoreContext from '../lib/stores/context'
import { Link } from 'react-router-dom'
import { RouteComponentProps } from 'react-router';
import { capitalize } from '../lib/util'
import { upload } from '../lib/api/upload'

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
    setUploadStatus({fullStatus: e.currentTarget.files[0].name, link: ''})
  }

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    if (file) {
      setLoading(true)
      const response = await upload(API, type, file, {
        name, url, token: enterpriseToken
      })
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
      </Hero>
      <div className="upload-wrapper">
        <Paper className="upload-form-wrapper">
          <Typography variant="title" className="upload-heading">
            Enter a name and upload a <code>.tgz</code> or <code>.tar.gz</code> file to create a new {type.substring(0, type.length - 1)}.
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
              label={`${capitalize(type)} Name`}
              helperText="If no value is entered, a default will be chosen from the source YAML file."
              InputLabelProps={{ shrink: true }}
            />
            <div style={{ margin: '0.5rem 0' }} />
            {type === 'operators' &&
              <TextField
                value={url}
                onChange={(e: ChangeEvent<HTMLInputElement>) => setUrl(e.currentTarget.value)}
                fullWidth
                margin="dense"
                variant="outlined"
                autoCorrect="false"
                label={`${capitalize(type)} GitHub or OperatorHub URL`}
                helperText="If no value is entered, a default will be chosen from the source YAML file."
                InputLabelProps={{ shrink: true }}
              />
            }
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
            {!file ? 
              <div className="filePicker-wrapper">
                <Button 
                  className="hero-buttons upload-button" 
                  variant="contained" 
                  color="primary">
                  <Icon>cloud_upload</Icon>
                  {` Select File`}
                </Button>
                <input 
                  type="file" 
                  name="component-file"
                  onChange={handleFile}
                  accept=".tgz, .gz"
                />
              </div>
              :
              <div className="filePicker-wrapper">
                <Button 
                  className="hero-buttons upload-button" 
                  variant="contained" 
                  color="primary"
                  type="submit"
                >
                  <Icon>cloud_upload</Icon>
                  {`Upload`}
                </Button>
              </div>
            }
          </form>
          { uploadStatus.link ?
            <Link to={`/${type}/${uploadStatus.link}`}>
              <p className="selected-file">{uploadStatus.fullStatus}</p>
            </Link> :
            <p className="selected-file">{uploadStatus.fullStatus}</p> 
          }
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
        </Paper>
      </div>
    </div>
  )
}

export default UploadPage