// Copyright 2021 IBM Corporation 
// 
// SPDX-License-Identifier: Apache-2.0
import { combineReducers } from './util'
import ArtifactReducer, { ArtifactInitial } from './artifacts'
import PageReducer, { PageInitial } from './pages'
import SettingsReducer, { SettingsInitial } from './settings'
import CustomPipelineReducer, { CustomPipelineInitial } from './pipeline'


export const initial = {
  artifacts: ArtifactInitial,
  pages: PageInitial,
  settings: SettingsInitial,
  pipeline: CustomPipelineInitial
}

const reducers = {
  artifacts: ArtifactReducer,
  pages: PageReducer,
  settings: SettingsReducer,
  pipeline: CustomPipelineReducer
}

export default combineReducers(reducers)
