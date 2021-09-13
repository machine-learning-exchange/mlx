// Copyright 2021 IBM Corporation
// 
// SPDX-License-Identifier: Apache-2.0
import { ArtifactAction, ArtifactState } from './artifacts'
import { PageAction } from './pages'
import { SettingsAction } from './settings'

export type State = { [key: string]: any }
export interface Action {
  type: string,
  [prop: string]: any
}
// export type Action = ArtifactAction | PageAction | SettingsAction

export type Reducer = (state: State, action: Action) => State
export type ReducerMap = { [key: string]: Reducer }
