// Copyright 2021 The MLX Contributors
// 
// SPDX-License-Identifier: Apache-2.0
import { State, Action, Reducer, ReducerMap } from './types'


export function combineReducers(reducers: ReducerMap): Reducer {
  return (s: State, a: Action) => {
    const states = Object.entries(reducers)
      .map(([ name, reducer ]) => [name, reducer(s[name], a)])
    return Object.fromEntries(states)
  }
}

export function withPersistence(name: string, reducer: Reducer): Reducer {
  return (state: State, action: Action) => persist(name, reducer(state, action))
}

export function persist(name: string, state: State): State {
  localStorage.setItem(name, JSON.stringify(state))
  return state
}
