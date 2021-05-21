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
import React, { useState, Dispatch, SetStateAction, useContext, useEffect } from 'react'
import StoreContext from '../lib/stores/context'
import { fetchArtifact } from '../lib/api/artifacts';
import { Artifact, FETCH_ARTIFACT_ASSETS } from '../lib/stores/artifacts'
import { SET_ACTIVE_PAGE } from '../lib/stores/pages';
import { ADD_COMPONENTS_TO_CART, REMOVE_COMPONENTS_OF_TYPE_FROM_CART } from '../lib/stores/pipeline';
import { capitalize, getUserInfo, hasRole, canShow } from '../lib/util';
import Hero from '../components/Hero'
import Button from '../components/Button'
import Icon from '@material-ui/core/Icon'
import Link from '../components/Link'
import checkmark from '../images/checkmark-outline.png'
import cancel from '../images/cancel-outline.png'
import predictorIcon from '../images/predictor-icon.png'
import explainerIcon from '../images/explainer-icon.png'
import transformerIcon from '../images/transformer-icon.png'
import tfLogo from '../images/tf-logo.png'
import kerasLogo from '../images/keras-logo.png'
import pytorchLogo from '../images/pytorch-logo.png'
import sklearnLogo from '../images/scikit-learn-logo.png'
import kubeflowLogo from '../images/kubeflow-logo.png'
import {
   Paper, TableHead, TableRow, TableCell, TableSortLabel,
  Table, TableBody, Toolbar, Typography, withStyles, WithStyles
} from '@material-ui/core';

interface MetaAllPageProps extends WithStyles<typeof styles> {
  type: string
  tagName: string
  getTag: (asset: Artifact) => string
  description: string
  runningStatus: string
  statusIcon: string
  alternateBG: boolean
  leftBtn: string
  leftLink: string
  leftIcon?: string
  leftAdmin?: boolean
  rightBtn: string
  rightLink: string
  rightIcon?: string
  rightAdmin?: boolean
  canEdit?: boolean
}
enum SortOrder {
  ASC = 'asc',
  DESC = 'desc'
}
const styles = {
  checkbox: {
    color: '#1ccdc7'
  }
}

const isAdmin = hasRole(getUserInfo(), 'admin');

function MetaAllPage(props: MetaAllPageProps) {
  var {
    type,
    leftBtn, leftLink, leftIcon,
    rightBtn, rightLink, rightIcon,
    rightAdmin = false, leftAdmin = false,
  } = props
  const [ order ] = useState(SortOrder.DESC)
  const [ orderBy, setOrderBy ] = useState('name')
  const columns = [
    { id: 'name', label: `Name`, numeric: false },
    { id: 'status', label: 'Status', numeric: false },
    { id: 'timestamp', label: 'Date Created', numeric: false },
    { id: 'framework', label: 'Framework', numeric: false },
    { id: 'components', label: 'Components', numeric: false },
    { id: 'cat', label: 'Namespace', numeric: false },
  ]
  // console.log(columns)
  const { store, dispatch } = useContext(StoreContext)
  const { artifacts, settings, pipeline } = store
  const assets: {[key: string]: any} = Object.fromEntries(artifacts[type] || []
    .map((asset: any) => [asset.metadata.name, asset]))
  const API = settings.endpoints.api.value || settings.endpoints.api.default
  const namespace = settings.kfserving.namespace.value || settings.kfserving.namespace.default
  useEffect(() => {
    fetchArtifact(API, type, namespace)
      .then(assets => dispatch({
        type: FETCH_ARTIFACT_ASSETS,
        assetType: type,
        assets
      }))
      dispatch({
        type: SET_ACTIVE_PAGE,
        page: type
      })
  }, [API, namespace, dispatch, type])

  const selected: Set<string> = new Set(pipeline.components
    .filter((asset: Artifact) => asset.type === type)
    .map(({ id }: Artifact) => id))

  const handleSelectAllForPipeline = (event: React.ChangeEvent<HTMLInputElement>) =>
    dispatch((event.target.checked)
      ? { type: ADD_COMPONENTS_TO_CART, assets: Object.values(assets)}
      : { type: REMOVE_COMPONENTS_OF_TYPE_FROM_CART, artifactType: type})

  function getStatusIcon(asset: any) {
    let isReady = true;
    asset.status?.conditions.forEach((condition: any) => {
      if (condition.type === "Ready") {
        if (condition.status !== 'True') {
          isReady = false;
        }
      }
    })
    const icon = isReady ? checkmark : cancel
    return <img style={{marginLeft: '10px', marginTop: '10px'}} src={icon} alt={icon} height="15"/>
  }

  function getTags(asset: any) {
    let getPredictor = false;
    let getExplainer = false;
    let getTransformer = false;
    asset.status?.conditions.forEach((condition: any) => {
      if (condition.type === "DefaultPredictorReady") {
        getPredictor = true;
      }
      if (condition.type === "DefaultExplainerReady") {
        getExplainer = true;
      }
      if (condition.type === "DefaultTransformerReady") {
        getTransformer = true;
      }
    })
    const predictor = getPredictor ? predictorIcon : ""
    const explainer = getExplainer ? explainerIcon : ""
    const transformer = getTransformer ? transformerIcon : ""
    return (
      <div style={{display: 'flex', flexDirection: 'row'}}>
        <img style={{marginLeft: '10px', marginTop: '10px'}} src={predictor} alt={predictor} height="18"/>
        <img style={{marginLeft: '10px', marginTop: '10px'}} src={explainer} alt={explainer} height="18"/>
        <img style={{marginLeft: '10px', marginTop: '10px'}} src={transformer} alt={transformer} height="18"/>
      </div>
    )
  } 
  function getFramework(asset: any) {
    let framework = ""
    if (Object.keys(asset.spec.default.predictor)[0] === "tensorflow") {
      framework = tfLogo
    }
    else if (Object.keys(asset.spec.default.predictor)[0] === "pytorch") {
      framework = pytorchLogo
    }
    else if (Object.keys(asset.spec.default.predictor)[0] === "keras") {
      framework = kerasLogo
    }
    else if (Object.keys(asset.spec.default.predictor)[0] === "sklearn" || Object.keys(asset.spec.default.predictor)[0] === "scikit-learn") {
      framework = sklearnLogo
    }
    else {
      framework = kubeflowLogo
    }
    
    return <img style={{marginLeft: '10px', marginTop: '10px'}} src={framework} alt={framework} height="15"/>
  }

  function getTimestamp(asset: any) {
    let timestamp = new Date(asset.metadata.creationTimestamp)

    const dateTimeFormat = new Intl.DateTimeFormat('en', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
    console.log(dateTimeFormat.format(timestamp));
    let finalTimestamp = dateTimeFormat.format(timestamp)
    
    return <div style={{marginLeft: '10px', marginTop: '10px'}}>{finalTimestamp}</div>
  }
 
  function titleCase(str: String) {
    var splitStr = str.toLowerCase().split(' ');
    for (var i = 0; i < splitStr.length; i++) {
        // You do not need to check if i is larger than splitStr length, as your for does that for you
        // Assign it back to the array
        splitStr[i] = splitStr[i].charAt(0).toUpperCase() + splitStr[i].substring(1);     
    }
    // Directly return the joined string
    return splitStr.join(' '); 
  }
  return (
    <>
      <Hero
        title={`${type}`} 
        subtitle={`Deploy an ${type.slice(0, -1)}.`}
      >
        { canShow(leftAdmin, isAdmin) &&
        <Link to={leftLink}>
          <Button
            className="hero-buttons-outline"
            variant="outlined"
            color="primary"
          >
            {leftIcon && <Icon>{leftIcon}</Icon>}
            {leftBtn}
          </Button>
        </Link>
        }
        { canShow(rightAdmin, isAdmin) &&
        <Link to={rightLink}>
          <Button
            className="hero-buttons"
            variant="contained"
            color="primary"
          >
            {rightIcon && <Icon>{rightIcon}</Icon>}
            {rightBtn}
          </Button>
        </Link>
        }
      </Hero>
      <div style={{ margin: '1rem 0.8rem' }}>
        <Paper>
          <EnhancedToolbar
            type={type}
            numSelected={pipeline.components.length}
            toggleModal={(e: never) => {}}
          />
          <Table>
            <TableHeader
              type={type} 
              columns={columns}
              order={order}
              orderBy={orderBy}
              setOrderBy={setOrderBy}
              numSelected={selected.size}
              rowCount={Object.entries(assets).length}
              onSelectAllClick={handleSelectAllForPipeline}
            />
            <TableBody>
              {Object.values(assets).map(asset =>
                <TableRow
                  hover
                  tabIndex={-1}
                  key={asset.name}
                >
                  {/* <TableCell padding="checkbox">
                    <Checkbox
                      checked={selected.has(asset.id)}
                      onChange={handleSelectAssetForPipeline(asset)}
                      className={selected.has(asset.id) ? 'checkbox' : ''}
                    />
                  </TableCell> */}
                  <TableCell component="th" id={asset.id} scope="row" padding="dense" >
                    <Link to={asset.metadata.name}>{titleCase(asset.metadata.name.replace(/-/g, ' '))}</Link>
                  </TableCell>
                  <TableCell padding="dense">{getStatusIcon(asset)}</TableCell>
                  <TableCell padding="dense">{getTimestamp(asset)}</TableCell>
                  <TableCell padding="dense">{getFramework(asset)}</TableCell>
                  <TableCell padding="dense">{getTags(asset)}</TableCell>
                  <TableCell padding="dense">{asset.metadata.namespace}</TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </Paper>
      </div>
    </>
  )
}
interface TableHeaderProps {
  type: string
  columns: { id: string, label: string, numeric: boolean }[]
  order: SortOrder
  orderBy: string
  setOrderBy: Dispatch<SetStateAction<string>>
  numSelected: number
  rowCount: number
  onSelectAllClick: Dispatch<SetStateAction<any>>
}

function TableHeader(props: TableHeaderProps) {
  const {
    columns, order, orderBy,
    setOrderBy
  } = props
  return (
    <TableHead>
      <TableRow>
        {columns.map(({ id, label, numeric }) => 
          <TableCell
            key={id} 
            align={numeric ? 'right' : 'left'}
            sortDirection={orderBy === id ? order : false}
            padding="dense"
          >
            <TableSortLabel onClick={() => setOrderBy(id)}>{label}</TableSortLabel>
          </TableCell> 
        )}
      </TableRow>
    </TableHead>
  )
}
interface EnhancedToolbarProps {
  type: string
  numSelected: number
  toggleModal: (e: never) => void
}
function EnhancedToolbar(props: EnhancedToolbarProps) {
  const { type, numSelected } = props
  return (
    <Toolbar
      style={{
        display: 'flex',
        flexDirection: 'row',
        justifyContent: 'space-between'
      }}
    >
      <div>
        <Typography variant="h6" id="tableTitle">
          {numSelected
            ? `${capitalize(type)} (${numSelected} selected)`
            : `Select ${capitalize(type)} for your pipeline`}
        </Typography>
      </div>
    </Toolbar>
  )
}
export default withStyles(styles)(MetaAllPage)