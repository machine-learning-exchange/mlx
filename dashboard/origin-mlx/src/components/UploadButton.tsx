/*
* Copyright 2021 The MLX Contributors
*
* SPDX-License-Identifier: Apache-2.0
*/
import React, {
  useContext, useState, ChangeEvent, FormEvent, ReactNode,
} from 'react';
import { Link } from 'react-router-dom';
import { RouteComponentProps } from 'react-router';
import Icon from '@material-ui/core/Icon';
import Paper from '@material-ui/core/Paper';
import TextField from '@material-ui/core/TextField';
import Typography from '@material-ui/core/Typography';
import yaml from 'js-yaml';
import fs from 'fs';
import StoreContext from '../lib/stores/context';
import { capitalize } from '../lib/util';
import { upload } from '../lib/api/upload';
import Button from './Button';
import Hero from './Hero';
import indicatorGif from '../images/indicator-gif.gif';
import { UPDATE_ARTIFACT_ASSET, Artifact } from '../lib/stores/artifacts';
import { setFeaturedArtifacts, setPublishApprovedArtifacts } from '../lib/api/artifacts';

interface MatchProps {
  type: string
}

function UploadButton(props: RouteComponentProps<MatchProps>) {
  const { type } = props.match.params;
  const [name, setName] = useState('');
  const [url, setUrl] = useState('');
  const [enterpriseToken, setEnterpriseToken] = useState('');
  const [uploadStatus, setUploadStatus] = useState({ fullStatus: '', link: '' });
  const [file, setFile] = useState(null);
  const [serviceName, setServiceName] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { store, dispatch } = useContext(StoreContext);
  const { artifacts, settings } = store;
  const API = settings.endpoints.api.value || settings.endpoints.api.default;
  const isDeployed = false;
  const assets: { [key: string]: Artifact } = Object.fromEntries(artifacts[type]
    .map((asset: Artifact) => [asset.name, asset]));

  const handleFile = (e: ChangeEvent<HTMLInputElement>) => {
    setFile(e.currentTarget.files[0]);
    const fileReader = new FileReader();
    fileReader.onloadend = () => {
      if (typeof fileReader.result === 'string') {
        const service : any = yaml.safeLoad(fileReader.result);
        setServiceName(service.metadata && service.metadata.name || '');
      }
    };
    fileReader.readAsText(e.currentTarget.files[0]);
    setUploadStatus({ fullStatus: e.currentTarget.files[0].name, link: '' });
  };
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (file) {
      setLoading(true);
      const response = await upload(API, type, file, {
        name, url, token: enterpriseToken,
      });
      setLoading(false);
      if (response.status !== 200) { response.text().then((text) => {
        setError(text);
        setUploadStatus({ fullStatus: (`Deployment of ${file.name} failed`), link: '' });
      }); }
      else {
        const response_json = await response.json();
        // Makes the newly uploaded file publishable and featured
        const path = `${serviceName}`;
        console.log('path');
        console.log(path);
        setUploadStatus({ fullStatus: ('Deployment Suceeded: predictor starting now.'), link: path });
        // TODO: Publishable and featured properties deprecated for kfservices - will revisit this
        // publishable.add(path)
        // featured.add(path)
        // await setPublishApprovedArtifacts(API, type, Array.from(publishable.values()))
        //   .then(() => dispatch({
        //     type: UPDATE_ARTIFACT_ASSET, assetType: type,
        //     path, payload: { publish_approved: true }
        //   }))
        // await setFeaturedArtifacts(API, type, Array.from(featured.values()))
        //   .then(() => dispatch({
        //     type: UPDATE_ARTIFACT_ASSET, assetType: type,
        //     path, payload: { featured: true }
        //   }))
      }
      setFile(null);
    }
    for (let i = 0; i < artifacts.length; i += 1) {
      if (artifacts[i].status.conditions.type === 'DefaultPredictorReady') {
        console.log(artifacts[i].status.conditions.status);
        console.log(artifacts.length);
      }
    }
  };
  // var uploadFileName = artifacts[artifacts.length - 1].metadata.name
  console.log(uploadStatus);
  // const endpoint = `/${type}/upload?` + (name && `name=${name}`) + (url && `&url=${url}`)
  return (
    <div className="page-wrapper">
      <div className="upload-wrapper">
        <Paper style={{ height: '30%' }} className="upload-form-wrapper">
          <Typography variant="title" className="upload-heading">
            Deploy a
            {' '}
            <code>.yaml</code>
            {' '}
            file to create a new KFService.
          </Typography>
          <form
            method="post"
            encType="multipart/form-data"
            onSubmit={handleSubmit}
          >

            {type === 'inferenceservices' && isDeployed
              && (
              <TextField
                value={url}
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
              )}
            {!file
              ? (
                <div className="filePicker-wrapper">
                  <Button
                    className="hero-buttons upload-button"
                    variant="contained"
                    color="primary"
                  >
                    <Icon>cloud_upload</Icon>
                    {' Select File'}
                  </Button>
                  <input
                    type="file"
                    name="component-file"
                    onChange={handleFile}
                    accept=".tgz, .gz, .yaml"
                  />
                </div>
              )
              : (
                <>
                  <Button
                    className="hero-buttons upload-button"
                    variant="contained"
                    color="primary"
                    type="submit"
                  >
                    <Icon>cloud_upload</Icon>
                    Deploy
                  </Button>
                </>
              )}
          </form>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            { uploadStatus.link
              ? (
                <Link to={`/${type}/${uploadStatus.link}`}>
                  <div style={{
                    display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center',
                  }}
                  >
                    <p className="selected-file">Click to view service details.</p>
                    <img src={indicatorGif} style={{ width: '100px' }} alt="indicator gif" />
                  </div>
                </Link>
              )
              : <p className="selected-file">{uploadStatus.fullStatus}</p>}
            {error
            && (
            <p className="error-msg">
              {`Upload Error: Please Retry - ${error}`}
            </p>
            )}
          </div>

          {loading
              && (
              <p className="upload-msg">
                Uploading...
                <img src={indicatorGif} style={{ width: '100px' }} alt="indicator gif" />
              </p>
              )}
        </Paper>
      </div>
    </div>
  );
}
export default UploadButton;
