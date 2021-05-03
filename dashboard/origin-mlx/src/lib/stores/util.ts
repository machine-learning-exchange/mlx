// Copyright 2021 IBM Corporation
// 
// Licensed under the Apache License, Version 2.0 (the "License"); 
// you may not use this file except in compliance with the License. 
// You may obtain a copy of the License at 
// 
//     http://www.apache.org/licenses/LICENSE-2.0 
// 
// Unless required by applicable law or agreed to in writing, software 
// distributed under the License is distributed on an "AS IS" BASIS, 
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
// See the License for the specific language governing permissions and 
// limitations under the License. 
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
