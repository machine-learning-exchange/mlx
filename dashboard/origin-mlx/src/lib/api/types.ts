// Copyright 2021 The MLX Contributors
// 
// SPDX-License-Identifier: Apache-2.0
import { SettingsState } from '../stores/settings'

export interface SettingsPayload {
  sections: Section[]
}

export interface Section {
  name: string,
  description: string,
  settings: Setting<boolean | number | string>[]
}

export interface Setting<T> {
  name: string,
  description: string,
  default: T,
  value?: T
}

export type AppSettings = SettingsState
