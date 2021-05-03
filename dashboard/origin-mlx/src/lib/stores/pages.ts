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
import { State, Action } from "./types"

interface PageState extends State {
  active: string
}

const initial: PageState = {
  active: 'home'
}

export const SET_ACTIVE_PAGE = 'SET_ACTIVE_PAGE'

export interface SetActivePageAction extends Action {
  type: typeof SET_ACTIVE_PAGE
  page: string
}

export type PageAction = SetActivePageAction

function reducer(state: State, action: Action) {
  if (action as PageAction) {
    switch (action.type) {
      case SET_ACTIVE_PAGE: {
        const { page } = action as SetActivePageAction
        return { ...state, active: page }
      }
      default:
        return state
    }
  }
}

export default reducer
export { initial as PageInitial }
