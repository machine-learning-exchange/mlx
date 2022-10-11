/*
* Copyright 2021 The MLX Contributors
*
* SPDX-License-Identifier: Apache-2.0
*/
import React, {
  useContext, useState, ChangeEvent, FormEvent,
} from 'react';
import TextField from '@material-ui/core/TextField';
import StoreContext from '../../lib/stores/context';

import Button from '../Button';
import { requestArtifactRun, RunParameters } from '../../lib/api/run';

interface RunViewProps {
  type: string,
  asset: {
    [key: string]: any,
    parameters?: any[]
  }
  setRunLink?: Function
}

function RunView(props: RunViewProps) {
  const { asset, type } = props;

  const { store } = useContext(StoreContext);
  const { api, kfp } = store.settings.endpoints;
  const API = api.value ? api.value : api.default;
  const KFP = kfp.value ? kfp.value : kfp.default;
  const { setRunLink } = props;

  const shownParams: { [key: string]: any }[] = [];
  const matchedUrlParams: { [key: string]: string } = {};
  const matches: string[] = [];

  // Adds all parameters that don't already have a value (from the url)
  // to list of parameters which we will ask the user for
  if (asset.parameters) {
    for (let assetIter = 0; assetIter < asset.parameters.length; assetIter += 1) {
      let hasMatch = false;
      for (const key of Object.keys(asset.url_parameters)) {
        if (key === asset.parameters[assetIter].name) hasMatch = true;
      }
      // If there is no matching url_parameter add the parameter to the form
      if (!hasMatch) shownParams.push(asset.parameters[assetIter]);
      else matches.push(asset.parameters[assetIter].name);
    }
  }

  // Marks all url_parameters that have a match to be loaded to the payload
  Object.keys(asset.url_parameters).forEach((key: string) => {
    matches.forEach((match: string) => {
      if (key === match) matchedUrlParams[key] = asset.url_parameters[key];
    });
  });

  const [run, setRun] = useState({
    ...Object.fromEntries((shownParams || []).map(
      ({ name, value, default: defaultValue }) => [name, value || defaultValue || ''],
    )),
    runname: asset.name,
    link: undefined,
  });

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const { link, ...parameters } = run;

    const payload: RunParameters = { name: parameters.name };
    Object.keys(parameters).forEach((key: string) => {
      payload[key] = parameters[key];
    });
    Object.keys(matchedUrlParams).forEach((key: string) => {
      payload[key] = asset.url_parameters[key];
    });

    requestArtifactRun(API, type, asset.id, payload)
      .then(({ run_url }) => {
        setRunLink(`${KFP}/pipeline/#${run_url}`);
        setRun({ ...run, link: run_url });
      });
  }

  return (
    <div className="runview-wrapper">
      <div style={{ width: '98%', height: '100%', paddingRight: '2%' }}>
        {run.link
          ? (
            <div>
              <h2 className="run-form-title">View Trial Pipeline</h2>
              <p>The sample pipeline created for this model&#39;s trial run can be viewed at the following link:</p>
              <a target="_blank" rel="noopener noreferrer" href={`${KFP}/pipeline/#${run.link && run.link}`}>
                {`View '${run.runname || asset.name}' on Kubeflow Pipelines.`}
              </a>
            </div>
          )
          : (
            <div className="run-form">
              { type === 'operators'
                ? <h2 className="run-form-title">Install the Operator</h2>
                : <h2 className="run-form-title">Create a Trial Run</h2>}
              { type === 'operators' ? (
                <p>
                  Click Install to deploy the Operator
                </p>
              ) : (
                <p>
                  {`Complete the following inputs and hit 'Submit'
                to run the ${type} in a sample pipeline.`}
                </p>
              )}
              <form autoComplete="off" onSubmit={handleSubmit}>
                { type === 'operator' ? (
                  <TextField
                    autoCorrect="false"
                  // id='runName'
                  // className="run-name-input"
                    label="Operator Name"
                  // placeholder={asset.name}
                    helperText=""
                    value={run.runname}
                    fullWidth
                    margin="normal"
                    variant="outlined"
                    InputLabelProps={{ shrink: true }}
                    style={{ backgroundColor: 'blue !important' }}
                    onChange={(e: ChangeEvent<HTMLInputElement>) => setRun({ ...run, name: e.currentTarget.value })}
                  />
                ) : (
                  <TextField
                    autoCorrect="false"
                  // id='runName'
                  // className="run-name-input"
                    label="Run Name"
                  // placeholder={asset.name}
                    helperText="Enter a name to be used for the trial run."
                    value={run.runname}
                    fullWidth
                    margin="normal"
                    variant="outlined"
                    InputLabelProps={{ shrink: true }}
                    style={{ backgroundColor: 'blue !important' }}
                    onChange={(e: ChangeEvent<HTMLInputElement>) => setRun({ ...run, runname: e.currentTarget.value })}
                  />
                )}
                { type === 'datasets' && (
                <TextField
                  key="namespace"
                  label="Namespace"
                  helperText="Enter a namespace to be used"
                  value={run.namespace}
                  autoCorrect="false"
                  required
                  fullWidth
                  margin="normal"
                  style={{ marginBottom: '2%' }}
                  variant="outlined"
                  InputLabelProps={{ shrink: true }}
                  onChange={(e: ChangeEvent<HTMLInputElement>) => setRun({ ...run, namespace: e.currentTarget.value })}
                />
                )}
                { type === 'notebooks' && (
                <>
                  <TextField
                    key="dataset-pvc"
                    label="Dataset PVC"
                    helperText="Enter a dataset pvc to be used"
                    value={run['dataset-pvc']}
                    autoCorrect="false"
                    fullWidth
                    margin="normal"
                    style={{ marginBottom: '2%' }}
                    variant="outlined"
                    InputLabelProps={{ shrink: true }}
                    onChange={(e: ChangeEvent<HTMLInputElement>) => setRun({ ...run, dataset_pvc: e.currentTarget.value })}
                  />
                  <TextField
                    key="mount-path"
                    label="Mount Path"
                    helperText="Enter a mount path to be used"
                    value={run['mount-path']}
                    autoCorrect="false"
                    fullWidth
                    margin="normal"
                    style={{ marginBottom: '2%' }}
                    variant="outlined"
                    InputLabelProps={{ shrink: true }}
                    onChange={(e: ChangeEvent<HTMLInputElement>) => setRun({ ...run, mount_path: e.currentTarget.value })}
                  />
                </>
                )}
                {shownParams && shownParams.map(({ name, description }) => (
                  <TextField
                    key={name}
                  // className="run-name-input"
                    label={`Run ${name}`}
                  // placeholder={asset.id}
                    helperText={description || ''}
                    value={run[name]}
                    autoCorrect="false"
                    required={(description || '').includes('Required.')}
                    fullWidth
                    margin="normal"
                    style={{ marginBottom: '2%' }}
                    variant="outlined"
                    InputLabelProps={{ shrink: true }}
                    onChange={(e: ChangeEvent<HTMLInputElement>) => setRun({ ...run, [name]: e.currentTarget.value })}
                  />
                ))}
                <div className="submit-button-wrapper">
                  <Button
                  // onClick={ this.handleSubmit }
                    type="submit"
                    className="hero-buttons submit-run-button"
                    variant="contained"
                    color="primary"
                  >
                    Submit
                  </Button>
                </div>
                {/* <TextField
                select
                SelectProps={{ MenuProps: { MenuListProps: { style: { width: '100%' } } } }}
                label="Run Type"
                helperText="Select the type of trial run to perform."
                value={ this.state.runType }
                onChange={ this.handleChange('runType') }
                fullWidth
                style={{ marginBottom: '2%' }}
                className="model-run-item"
                name="runType">
                { this.getRunTypes().map((name:string, i:number)=>
                  <MenuItem key={ i } value={ name }>{ capitalized(name) }</MenuItem>
                )}
              </TextField>

              <TextField
                select
                SelectProps={{ MenuProps: { MenuListProps: { style: { width: '100%' } } } }}
                label="Platform"
                helperText="Select the platform to run your trial run on."
                value={ this.state.platform }
                onChange={ this.handleChange('platform') }
                className="model-run-item"
                fullWidth
                style={{ marginBottom: '2%' }}
                name="platform">
                { this.getPlatforms(this.state.runType).map((name:string, i:number) =>
                  <MenuItem key={ i } value={ name }>{ name.length > 3 ? capitalized(name) : name.toUpperCase() }</MenuItem>
                )}
              </TextField> */}
              </form>

              {/* { this.state.errorState ?
              <p className="error-msg">
                { `Run Error: Please Retry - ${ this.state.errorState }` }
              </p>
            :
              this.state.isLoading &&
              <p className="upload-msg">
                { `Loading...` }
              </p>
            } */}

            </div>
          )}
      </div>
    </div>
  );
}

export default RunView;
