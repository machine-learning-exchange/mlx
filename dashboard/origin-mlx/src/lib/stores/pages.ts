// Copyright 2021 The MLX Contributors
// 
// SPDX-License-Identifier: Apache-2.0
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
