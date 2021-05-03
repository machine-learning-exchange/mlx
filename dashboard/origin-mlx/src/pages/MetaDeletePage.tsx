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
import { Link } from 'react-router-dom'
import Hero from '../components/Hero';
import yaml from 'js-yaml';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Button from '@material-ui/core/Button';
import Icon from '@material-ui/core/Icon';

import { capitalize } from '../lib/util'


export interface IMetaDeleteProps {
  match: any;
  API: string;
  hasAssets?: boolean;
  alternateBG?: boolean;
  canRun?: boolean;
}

export default class MetaDelete extends React.Component<IMetaDeleteProps, any> {
  constructor(props:IMetaDeleteProps) {
    super(props)
    this.state = {
      assetType: this.props.match.params.type,
      assets: [],
      checked: [],
    };
  }
  
  componentDidMount() {
    this.getAssetList();
    // this.props.setActive(capitalize(this.state.assetType));
  }

  getThirdColName = (assetType:string) => {
    if (assetType === 'operators') {
      return 'Kind';
    } else if (assetType === 'components') {
      return 'Platform';
    } else if (assetType === 'pipelines') {
      return 'Category';
    } else if (assetType === 'models') {
      return 'Domain';
    }
  }

  getAssetList = async () => {
    const rawYAML = await fetch(`${this.props.API}/apis/v1alpha1/${this.state.assetType}`);
    const assets : any = yaml.safeLoad(await rawYAML.text());
    this.setState({ assets: assets[this.state.assetType] });
  }

  isChecked = (key:any) => {
    return this.state.checked.includes(key);
  }

  handleRowClick = (i:number) => () => {
    if (this.state.assetType === 'pipelines') {
      this.setState({
        selectedAsset: this.state.assets[i]
      });
    } else if (this.state.assetType === 'operators') {
      
    } else {
      this.toggleCheck(i)
      this.setState({
        selectedAsset: this.state.assets[i]
      });
    }
  }

  toggleCheck = (value:any) => {
    const { checked } = this.state;
    const currentIndex = checked.indexOf(value);
    const newChecked = [...checked];

    if (currentIndex === -1) {
      newChecked.push(value);
    } else {
      newChecked.splice(currentIndex, 1);
    }
    this.setState({
      checked: newChecked,
    });
  }

  deleteAsset = async (asset:any) => {
    try {
      this.setState({
        assets: this.state.assets.filter((target:any) => target.id !== asset.id)
      })
    } catch (e) {
      console.log(e);
    }
  }
  
  public render() {
    const { assetType } = this.state;

    return (
      <div className="page-wrapper">
        <Hero
          title={capitalize(assetType)}
          subtitle={`Click to delete a ${capitalize(assetType)}.`}
          alternate={this.props.alternateBG}
        >
          <Link to={`/${assetType}`}>
            <Button
              className="hero-buttons-outline"
              variant="outlined"
              color="primary"
            >
              {<Icon>arrow_back</Icon>}
              {assetType}
            </Button>
          </Link>
        </Hero>
        <div className="list-wrapper">
        <Table>
        <TableHead>
          <TableRow className='list-head-row'>
            <TableCell>{ capitalize(assetType.slice(0, assetType.length-1)) } Name</TableCell>
            <TableCell align="right">Description</TableCell>
            <TableCell align="right">{ this.getThirdColName(assetType) }</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          { this.state.assets && this.state.assets.map((row:any, i:number) => {
            let thirdColData;
            if (assetType === "models") {
              thirdColData = row.domain;
            } else if (assetType === "components") { 
              thirdColData = row.metadata?.annotation?.platform || 'OpenSource'
            } else if (assetType === "pipelines") { 
              thirdColData = row.category;
            } else if (assetType === "operators") { 
              thirdColData = row.kind;
            }
            return (
              !this.state.checked.includes(i) ?
              <TableRow 
                className="list-row"
                key={i}
                onClick={this.handleRowClick(i)}>
                <TableCell>
                  {row.name}
                </TableCell>
                <TableCell align="right">{row.description}</TableCell>
                <TableCell className="third-table-column" align="right">{thirdColData}</TableCell>
              </TableRow>
            :
              <TableRow 
                className="list-row confirm-delete"
                key={i}
                onClick={this.handleRowClick(i)}>
                <TableCell className="">
                  {row.name}
                </TableCell>
                <TableCell align="right">{`CLICK BUTTON TO DELETE `}<Icon>arrow_forward</Icon></TableCell> 
                <TableCell className="third-table-column" align="right">
                  <Button 
                    className="delete-button" 
                    variant="contained" 
                    onClick={() => this.deleteAsset(row)}
                    >
                    <span className="delete-button-text">DELETE</span>
                  </Button>
                </TableCell> 
              </TableRow>

            )
          })}
        </TableBody>
        </Table>
      </div>
    </div>
    );
  }
}
