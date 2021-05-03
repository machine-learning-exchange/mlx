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
import { fetchArtifact, setFeaturedArtifacts, setPublishApprovedArtifacts } from '../lib/api/artifacts';
import { Artifact, FETCH_ARTIFACT_ASSETS, UPDATE_ARTIFACT_ASSET } from '../lib/stores/artifacts'
import { SET_ACTIVE_PAGE } from '../lib/stores/pages';
import { ADD_COMPONENTS_TO_CART, REMOVE_COMPONENTS_OF_TYPE_FROM_CART, ADD_COMPONENT_TO_CART, REMOVE_COMPONENT_FROM_CART } from '../lib/stores/pipeline';
import { capitalize } from '../lib/util';

import Hero from '../components/Hero'
import Button from '../components/Button'
import Icon from '@material-ui/core/Icon'
import Link from '../components/Link'
import {
  Checkbox, Paper, TableHead, TableRow, TableCell, TableSortLabel,
  Table, TableBody, Toolbar, Typography, withStyles, WithStyles
} from '@material-ui/core';


interface MetaAllPageProps extends WithStyles<typeof styles> {
  type: string
  tagName: string
  getTag: (asset: Artifact) => string
  description: string
  alternateBG: boolean
  leftBtn: string
  leftLink: string
  leftIcon?: string
  rightBtn: string
  rightLink: string
  rightIcon?: string
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

function MetaAllPage(props: MetaAllPageProps) {
  const {
    type,
    tagName, getTag,
    leftBtn, leftLink, leftIcon,
    rightBtn, rightLink, rightIcon,
    canEdit,
  } = props

  const [ order ] = useState(SortOrder.DESC)
  const [ orderBy, setOrderBy ] = useState('name')

  const columns = [
    { id: 'name', label: `${capitalize(type).substring(0, type.length-1)} Name`, numeric: false },
    { id: 'desc', label: 'Description', numeric: false },
    { id: 'feat', label: 'Featured', numeric: false },
    { id: 'pub', label: 'Published', numeric: false },
    { id: 'cat', label: tagName, numeric: false },
  ]

  const { store, dispatch } = useContext(StoreContext)
  const { artifacts, settings, pipeline } = store
  const assets: {[key: string]: Artifact} = Object.fromEntries((artifacts[type] || [])
    .map((asset: Artifact) => [asset.name, asset]))

  const API = settings.endpoints.api.value || settings.endpoints.api.default

  useEffect(() => {
    fetchArtifact(API, type)
      .then(assets => dispatch({
        type: FETCH_ARTIFACT_ASSETS,
        assetType: type,
        assets
      }))

      dispatch({
        type: SET_ACTIVE_PAGE,
        page: type
      })
  }, [API, type, dispatch])

  const featured = new Set(Object.entries(assets)
    .filter(([_, asset]) => asset.featured)
    .map(([_, asset]) => asset.id))

  const publishable = new Set(Object.entries(assets)
    .filter(([_, asset]) => asset.publish_approved)
    .map(([_, asset]) => asset.id))

  const selected: Set<string> = new Set(pipeline.components
    .filter((asset: Artifact) => asset.type === type)
    .map(({ id }: Artifact) => id))

  const handleCheckFeatured = async (id: string, change: { featured: boolean } ) => {
    if (!canEdit)
      return

    if (change.featured)
      featured.add(id)
    else
      featured.delete(id)

    await setFeaturedArtifacts(API, type, Array.from(featured.values()))
      .then(() => dispatch({
        type: UPDATE_ARTIFACT_ASSET, assetType: type,
        id, payload: { featured: change.featured }
      }))
  }

  const handleCheckPublishApproved = async (id: string, change: { approved: boolean } ) => {
    if (!canEdit)
      return
      
    if (change.approved)
      publishable.add(id)
    else
      publishable.delete(id)

    await setPublishApprovedArtifacts(API, type, Array.from(publishable.values()))
      .then(() => dispatch({
        type: UPDATE_ARTIFACT_ASSET, assetType: type,
        id, payload: { publish_approved: change.approved }
      }))
  }

  const handleSelectAllForPipeline = (event: React.ChangeEvent<HTMLInputElement>) =>
    dispatch((event.target.checked)
      ? { type: ADD_COMPONENTS_TO_CART, assets: Object.values(assets)}
      : { type: REMOVE_COMPONENTS_OF_TYPE_FROM_CART, artifactType: type})

  const handleSelectAssetForPipeline = (asset: Artifact) =>
    (event: React.ChangeEvent<HTMLInputElement>) =>
      dispatch((event.target.checked)
        ? { type: ADD_COMPONENT_TO_CART, asset}
        : { type: REMOVE_COMPONENT_FROM_CART, id: asset.id })

  
  // console.log(pipeline.components.map(({ type }: Artifact) => type))

  return (
    <>
      <Hero
        title={`${type}`} 
        subtitle={`Upload a ${type}`}
      >
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
                  <TableCell padding="checkbox">
                    <Checkbox
                      checked={selected.has(asset.id)}
                      onChange={handleSelectAssetForPipeline(asset)}
                      className={selected.has(asset.id) ? 'checkbox' : ''}
                    />
                  </TableCell>
                  <TableCell component="th" id={asset.id} scope="row" padding="dense" >
                    {asset.name}
                  </TableCell>
                  <TableCell padding="dense">{asset.description}</TableCell>
                  <TableCell padding="dense">
                    <Checkbox
                      checked={asset.featured as boolean}
                      disabled={!canEdit || !asset.publish_approved}
                      onChange={() => handleCheckFeatured(asset.id, { featured: !asset.featured })}
                      className={!canEdit || !asset.publish_approved ? '' : 'checkbox'}
                    />
                  </TableCell>
                  <TableCell padding="dense">
                    <Checkbox
                      checked={asset.publish_approved as boolean}
                      disabled={!canEdit}
                      onChange={() => handleCheckPublishApproved(asset.id, { approved: !asset.publish_approved })}
                      className={!canEdit || !asset.publish_approved ? '' : 'checkbox'}
                    />
                  </TableCell>
                  <TableCell padding="dense">{getTag(asset)}</TableCell>
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
    columns,
    order, orderBy, setOrderBy,
    numSelected, rowCount, onSelectAllClick
  } = props

  return (
    <TableHead>
      <TableRow>
        <TableCell padding="checkbox">
          <Checkbox
            indeterminate={numSelected > 0 && numSelected < rowCount}
            checked={rowCount > 0 && numSelected === rowCount}
            onChange={onSelectAllClick}
            className={numSelected === rowCount ? 'checkbox' : ''}
          />
        </TableCell>
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
