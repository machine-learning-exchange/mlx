/* 
* Copyright 2021 The MLX Contributors
* 
* SPDX-License-Identifier: Apache-2.0
*/ 
import * as React from 'react';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import Switch from '@material-ui/core/Switch';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Select from '@material-ui/core/Select';
import LinearProgress from '@material-ui/core/LinearProgress'

export interface IDataListItemProps {
  name?: string;
  data?: string;
  defaultData?: string;
  options?: Array<any>;
  savedValue?: string;
  thirdColData?: string;
  itemClass?: string;
  stripUnderscore?: boolean;
  capitalizeData?: boolean;
  noDividider?: boolean;
  handleSelect?: Function;
  handleClick?: Function;
  handleType?: Function;
  saveValue?: Function;
  handleFile?: Function;
  progress?: number;
}

export default function DataListItem (props: IDataListItemProps) {
  return (
    <div>
      <Grid container>
        <Grid item xs={3}>
          <dt>
            <Typography 
              variant="subtitle1" 
              className="model-meta-heading">
              { props.name || `` }
            </Typography>
          </dt>
        </Grid>
        <Grid item xs={props.thirdColData ? 6 : 9}>
          <dd className="param-text">
            { buildItem(props) }
          </dd>
        </Grid>
        {props.thirdColData &&
            <Grid item xs={3}>
              <dd className="param-text">
                <Typography 
                    variant="subheading">
                  { props.thirdColData }
                </Typography>
              </dd>
            </Grid>
        }
        {props.defaultData && 
          <Grid container>
            <Grid item xs={3}>
              <dt className="default">
                <b>default</b>
              </dt>
            </Grid>
            <Grid item xs={9}>
              <dd className="param-text default">
                { props.defaultData }
              </dd>
            </Grid>
          </Grid>
        }
      </Grid>
      <hr className="parameter-divider"/>
    </div>
  );
}

const buildItem = (props:any) => {
  const { name, 
    itemClass, 
    data, 
    options, 
    savedValue, 
    handleClick, 
    handleType, 
    handleSelect, 
    saveValue,
    handleFile,
    progress
  } = props;

  if (itemClass === 'model-link') {
    return (
      <Typography variant="subheading">
        <a
          className={ itemClass }
          target="_blank"
          rel="noopener noreferrer"
          href={data}>   
          { data || `` }
        </a>
      </Typography>
    )
  } else if (itemClass === 'drop-down') {
    return (
        <Select
          native
          value={ data }
          onChange={ handleSelect(name) }>
          { options.map((opt:any, i:number) => <option key={i} value={opt}>{opt}</option>) }
        </Select>      
    )
  } else if (itemClass === 'toggle-switch') {
    return (
      <FormControlLabel
        className={ `settings-toggle ${ Boolean(data) ? `checked` : `unchecked` }` }
        control={
          <Switch 
            value={ name }
            checked={ Boolean(data) } 
            onChange={ handleClick(name) }
          />
        }
        label={String(data)}
      />
    )
  } else if (itemClass === 'text-input') {
    return (
      <span className='text-input-settings-wrapper'>
        <TextField
          autoCorrect="false"
          className=""
          placeholder={ savedValue }
          value={ data }
          variant="outlined"
          margin="dense"
          InputLabelProps={{
            shrink: true,
          }}
          onChange={ handleType(name) }
        />    
        { data !== savedValue &&
          <Button 
            className='text-input-settings-save'
            onClick={ saveValue(name) } >
            save
          </Button>
        }
      </span>
    )
  } else if (itemClass === 'file-button') {
    if (!progress && progress !== 0) {
      return (
        <div className="file-button-wrapper">
          <Button 
            className="hero-buttons upload-button" 
            variant="contained" 
            color="primary">
            {`Choose Catalog`}
          </Button>
          <input 
            type="file"
            name="component-file"
            onChange={ handleFile }
            accept=".json"
          />
        </div>
      )
    }
    else {
      return (
        <>
          <LinearProgress variant="determinate" value={progress}/>
          <Typography variant="body2" color="textSecondary">{`${Math.round(
            progress,
          )}%`}</Typography>
        </>
      )
    }
  } else if (itemClass === 'button') {
    return (
      <Button
        className="hero-buttons upload-button" 
        variant="contained" 
        color="primary"
        onClick={handleClick}
      >
        {name}
      </Button>
    )
  } else {
    return (
      <Typography 
        className={ itemClass }
        variant="subheading">
        { data || `` }
      </Typography>
    )
  }
}
