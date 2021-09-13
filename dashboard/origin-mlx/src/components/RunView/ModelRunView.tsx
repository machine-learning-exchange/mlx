/*
* Copyright 2021 IBM Corporation
* 
* SPDX-License-Identifier: Apache-2.0
*/ 
import React from 'react';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import MenuItem from '@material-ui/core/MenuItem';

const capitalized = (inputString:string) => inputString.split("").map((ltr, pos) => pos === 0 ? ltr.toUpperCase() : ltr).join("");

interface ModelRunFormProps {
  id: string
  servableCredentialsRequired: boolean
  trainableCredentialsRequired: boolean
  trainingPlatforms: Array<string>
  servingPlatforms: Array<string>;
  inputParameters: {[key: string]: string}[];
  urlParameters: {[key: string]: string}
  KFP: string
  API: string
  setRunLink?: Function
}

export default class ModelRunForm extends React.Component<ModelRunFormProps, any> {

  constructor(props:any) {
    super(props);

    var shownParams: {[key: string]: {description: string, value: string}} = {}
    var matchedUrlParams: {[key: string]: string} = {}
    var matches: string[] = []

    // Adds all parameters that don't already have a value (from the url)
    // to list of parameters which we will ask the user for
    if (props.inputParameters) {
      for(var yamlParamIter = 0; yamlParamIter < props.inputParameters.length; yamlParamIter++) {
        let hasMatch = false
        let curParam = props.inputParameters[yamlParamIter]
        Object.keys(props.urlParameters).forEach((key: string) => {
          if (key === curParam.name)
            hasMatch = true
        })
        // If there is no matching url_parameter add the parameter to the form
        if (!hasMatch)
          shownParams[curParam.name] = {description: curParam.description, value: curParam.default}
        else
          matches.push(curParam.name)
      }
    }

    // Marks all url_parameters that have a match to be loaded to the payload
    Object.keys(props.urlParameters).forEach((key: string) => {
      matches.forEach((match: string) => {
        if (key === match)
          matchedUrlParams[key] = props.urlParameters[key]
      })
    })
    this.state = {
      isLoading: false,
      errorState: '',
      shownParameters: shownParams,
      matchedUrlParameters: matchedUrlParams,
      runLink: '',
      runName: '',
      runToken: '',
      runUrl: '',
      runType: this.getRunTypes()[0],
      platform: ''
    };
  }

  componentDidMount = () => {
    document.getElementById('runName').focus()
    this.setState({
      platform: this.getPlatforms(this.state.runType)[0]
    })
  }

  getRunTypes = () => {
    let types = [];
    if (this.props.trainingPlatforms.length) 
      types.push('training');
    if (this.props.servingPlatforms.length) 
      types.push('serving');
    return types;
  }

  getPlatforms = (runType:string) => {
    if (runType === 'training') 
      return this.props.trainingPlatforms.filter(platform => platform !== "knative")
    if (runType === 'serving') 
      return this.props.servingPlatforms.filter(platform => platform !== "knative")
  }

  handleSubmit = async (e:any) => {
    e.preventDefault();
    let errorState = '';
    let runLink = '';
    const stage = this.state.runType === 'serving' ? 'serve' : 'train';
    const nameParam = this.state.runName ? `&run_name=${ this.state.runName }` : ``;
    const setRunLink = this.props.setRunLink

    var postBody: {[key: string]: string} = {
      github_token: this.state.runToken,
      github_url: this.state.runUrl
    }

    Object.keys(this.state.shownParameters).forEach((key: string) => {
      postBody[key] = this.state.shownParameters[key].value
    });

    if (this.state.matchedUrlParameters)
      Object.keys(this.state.matchedUrlParameters).forEach((key: string) => {
        postBody[key] = this.state.matchedUrlParameters[key]
      });

    const options = {
      headers: {
        'Accept': 'application/json',
        'Content-type': 'application/json'
      },
      method: 'POST',
      body: JSON.stringify(postBody)
    };
    try {
      this.setState({
        isLoading: true
      });
      const runResult = await fetch(`${this.props.API}` +
        `/apis/v1alpha1/models/${this.props.id}/run?` +
        `pipeline_stage=${stage}&execution_platform=${this.state.platform}${nameParam}`
      , options);
      if (runResult.status === 200) {
        const { run_url } = await runResult.json();
        setRunLink(`${this.props.KFP}/pipeline/#` + run_url)
        runLink = run_url;
      } else {
        errorState = String(runResult.statusText);
      }
      this.setState({
        runLink,
        errorState,
        isLoading: false
      });
    } catch (e) {
      console.log(`Model trial run creation: ${ e }`);
    }
  }
  
  handleChange = (field:string) => (event:any) => {
    this.setState({ [field]: event.target.value });
  }

  public render() {
    const { id } = this.props;
    return (
      <div className="runview-wrapper">
        <div style={{ width: '98%', height: '100%', paddingRight: '2%' }}>
          { this.state.runLink ?
            <div>
              <h2 className="run-form-title">View Trial Pipeline</h2>  
              <p>The sample pipeline created for this model's trial run can be viewed at the following link:</p>
              <a target="_blank" rel="noopener noreferrer" href={`${ this.props.KFP }/pipeline/#` + this.state.runLink}>{`View '${this.state.runName || this.props.id}' on Kubeflow Pipelines.`}</a>
            </div> 
          :
            <div>
              <h2 className="run-form-title">Create a Trial Run</h2>
              <p>
                Complete the following inputs and hit 'Submit'
                to run the model in a sample pipeline.
              </p>
              <form autoComplete="off">
              <TextField
                  select
                  SelectProps={{ MenuProps: { MenuListProps: { style: { width: '100%' } } } }}
                  label="Launch Type"
                  helperText="Select the type of trial run to perform."
                  value={ this.state.runType }
                  onChange={ this.handleChange('runType') }
                  fullWidth
                  style={{ marginBottom: '2%' }}
                  className="model-run-item"
                  name="runType">
                  {this.getRunTypes().map((name: string, i: number)=>
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
                </TextField>
                <TextField
                  autoCorrect="false"
                  id='runName'
                  className="run-name-input"
                  label='Run Name'
                  placeholder={ id }
                  helperText='Enter a name to be used for the trial run.'
                  value={ this.state.runName }
                  fullWidth
                  margin="normal"
                  style={{ marginBottom: '2%' }}
                  variant="outlined"
                  InputLabelProps={{ shrink: true }}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => this.setState({ runName: e.currentTarget.value})}
                />
                { this.state.shownParameters &&
                    Object.keys(this.state.shownParameters).map((key: string) => {
                    return (
                      <TextField
                        key={key}
                        className="run-name-input"
                        autoCorrect="false"
                        // id='runName'
                        // className="run-name-input"
                        label={key}
                        // placeholder={asset.name}
                        helperText={this.state.shownParameters[key].description}
                        value={this.state.shownParameters[key].value}
                        fullWidth
                        margin="normal"
                        variant="outlined"
                        InputLabelProps={{ shrink: true, }}
                        onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                          this.setState({
                            shownParameters: {
                              ...this.state.shownParameters,
                              [key]: {description: this.state.shownParameters[key].description, value: e.currentTarget.value}
                            }
                          })
                        }}
                      />
                    )
                  })
                }
                {(this.props.servableCredentialsRequired || this.props.trainableCredentialsRequired) &&
                  <>
                    <TextField
                      autoCorrect="false"
                      id='runToken'
                      className="run-name-input"
                      label='Run GitHub Token'
                      placeholder={ id }
                      helperText='Enter your GitHub Token (may be required).'
                      value={ this.state.runToken}
                      fullWidth
                      margin="normal"
                      style={{ marginBottom: '2%' }}
                      variant="outlined"
                      InputLabelProps={{ shrink: true }}
                      onChange={(e: React.ChangeEvent<HTMLInputElement>) => this.setState({ runToken: e.currentTarget.value})}
                    />
                    <TextField
                      autoCorrect="false"
                      id='runUrl'
                      className="run-name-input"
                      label='Run GitHub URL'
                      placeholder={ id }
                      helperText='Enter your GitHub URL (may be required).'
                      value={ this.state.runUrl }
                      fullWidth
                      margin="normal"
                      style={{ marginBottom: '2%' }}
                      variant="outlined"
                      InputLabelProps={{ shrink: true }}
                      onChange={(e: React.ChangeEvent<HTMLInputElement>) => this.setState({ runUrl: e.currentTarget.value})}
                    />
                  </>
                }
                </form>

                { this.state.errorState ?
                <p className="error-msg">
                  { `Run Error: Please Retry - ${ this.state.errorState }` }
                </p>
              : 
                this.state.isLoading &&
                <p className="upload-msg">
                  { `Loading...` }
                </p>
              }
                { !this.state.isLoading &&
                  <div className="submit-button-wrapper">
                    <Button 
                      onClick={ this.handleSubmit }
                      type="submit" 
                      className="hero-buttons submit-run-button" 
                      variant="contained" 
                      color="primary">
                      Submit
                    </Button>
                  </div>
                }
            </div>
          }
        </div>
      </div>
    );
  }
};
