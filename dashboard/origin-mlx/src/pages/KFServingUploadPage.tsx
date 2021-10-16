/* 
* Copyright 2021 The MLX Contributors
* 
* SPDX-License-Identifier: Apache-2.0
*/ 
import React, { useContext, useState, ChangeEvent, FormEvent } from 'react'
import StoreContext from '../lib/stores/context'
import { Link } from 'react-router-dom'
import { upload } from '../lib/api/upload'
import Button from '../components/Button'
import Icon from '@material-ui/core/Icon'
import Hero from '../components/Hero'
import Paper from '@material-ui/core/Paper'
import Typography from '@material-ui/core/Typography'
import indicatorGif from '../images/indicator-gif.gif'
import yaml from 'js-yaml';

  
function UploadPage() {
  const type = 'inferenceservices'
  const [ uploadStatus, setUploadStatus] = useState({fullStatus: '', link: ''})
  const [ file, setFile ] = useState(null)
  const [ serviceName, setServiceName ] = useState(null)
  const [ loading, setLoading ] = useState(false)
  const [ error, setError ] = useState('')
  const { store } = useContext(StoreContext)
  const { artifacts, settings } = store
  const API = settings.endpoints.api.value || settings.endpoints.api.default

  const handleFile = (e: ChangeEvent<HTMLInputElement>) => {
    setFile(e.currentTarget.files[0])
    setError('')
    const fileReader = new FileReader();
    fileReader.onloadend = () => {
      if (typeof fileReader.result === 'string') {
        const service : any = yaml.safeLoad(fileReader.result)
        setServiceName(service.metadata?.name || "")
      }
    }
    fileReader.readAsText(e.currentTarget.files[0]);
    setUploadStatus({fullStatus: e.currentTarget.files[0].name, link: ''})
  }
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    if (file) {
      setLoading(true)
      const response = await upload(API, type, file, {})
      setLoading(false)
      if (response.status < 200 || response.status >= 300)
        response.text().then(text => {
          setError(text)
          setUploadStatus({fullStatus: ("Deployment of " + file.name + " failed"), link: ''})
        })
      else{
        // Makes the newly uploaded file publishable and featured
        const path = `${serviceName}`
        setUploadStatus({fullStatus: ("Deployment Suceeded: predictor starting now."), link: path})
      }
      setFile(null)
    }
    for (var i=0; i< artifacts.length; i++) {
      if (artifacts[i].status.conditions.type === "DefaultPredictorReady") {
        console.log(artifacts[i].status.conditions.status)
        console.log(artifacts.length)
      }
    }
  }
  return (
    <div className="page-wrapper">
      <Hero
        title="KFServices"
        subtitle={`Deploy a KFService.`}
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
        <Paper style={{height: '30%'}} className="upload-form-wrapper">
          <Typography variant="title" className="upload-heading">
            Deploy a <code>.yaml</code> file to create a new KFService.
          </Typography>
          <form
            method="post" 
            encType="multipart/form-data"
            onSubmit={handleSubmit}
          >
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
                  accept=".tgz, .gz, .yaml, .yml"
                />
              </div>
              :
              <>
                <Button 
                  className="hero-buttons upload-button" 
                  variant="contained" 
                  color="primary"
                  type="submit"
                >
                  <Icon>cloud_upload</Icon>
                  {`Deploy`}
                </Button>
              </>
            }
          </form>
          <div style={{display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
          { uploadStatus.link ?
            <Link to={`/${type}/${uploadStatus.link}`}>
              <div style={{display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center'}}>
                <p className="selected-file">Click to view service details.</p>
              </div>
            </Link> :
            <p className="selected-file">{uploadStatus.fullStatus}</p> 
          }
          {error && 
            <p className="error-msg">
              {`Upload Error: Please Retry - ${error}`}
            </p>
          }
          </div>

          {loading && !uploadStatus.link &&
            <p className="upload-msg">
              `Uploading...
              <img src={indicatorGif} style={{width: '100px'}} alt="indicator gif"/>
            </p>
          }
        </Paper>
      </div>
    </div>
  )
}
export default UploadPage