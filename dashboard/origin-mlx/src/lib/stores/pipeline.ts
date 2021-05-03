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
import { State, Action } from './types'
import { Artifact } from './artifacts'


export interface CustomPipelineState extends State {
  components: Artifact[]
}

const initial: CustomPipelineState = {
  components: []
}


export const ADD_COMPONENT_TO_CART = 'ADD_COMPONENT_TO_CART'
export const ADD_COMPONENTS_TO_CART = 'ADD_COMPONENTS_TO_CART'
export const REMOVE_COMPONENT_FROM_CART = 'REMOVE_COMPONENT_FROM_CART'
export const REMOVE_COMPONENTS_OF_TYPE_FROM_CART = 'REMOVE_COMPONENTS_OF_TYPE_FROM_CART'
export const REORDER_COMPONENT_IN_CART = 'REORDER_COMPONENT_IN_CART'

export interface AddComponentToCartAction extends Action {
  type: typeof ADD_COMPONENT_TO_CART
  asset: Artifact
}

export interface AddComponentsToCartAction extends Action {
  type: typeof ADD_COMPONENTS_TO_CART
  assets: Artifact[]
}

export interface RemoveComponentFromCartAction extends Action {
  type: typeof REMOVE_COMPONENT_FROM_CART
  id: string
}

export interface RemoveComponentsOfTypeFromCart extends Action {
  type: typeof REMOVE_COMPONENTS_OF_TYPE_FROM_CART
  artifactType: string
}

export interface ReorderComponentInCartAction extends Action {
  type: typeof REORDER_COMPONENT_IN_CART
  id: string
  position: number
}

export type CustomPipelineAction =
  AddComponentToCartAction | RemoveComponentFromCartAction | ReorderComponentInCartAction |
  AddComponentsToCartAction | RemoveComponentsOfTypeFromCart 

function reducer(state: State, action: Action) {
  if (action as CustomPipelineAction) {
    switch (action.type) {
      case ADD_COMPONENT_TO_CART:
        return { ...state, components: state.components.concat(action.asset) }

      case ADD_COMPONENTS_TO_CART:
        return { ...state, components: state.components.concat(...action.assets) }

      case REMOVE_COMPONENT_FROM_CART:
        return {
          ...state,
          components: (state as CustomPipelineState).components
            .filter(({ id }) => id !== action.id)
        }

      case REMOVE_COMPONENTS_OF_TYPE_FROM_CART:
        return {
          ...state,
          components: (state as CustomPipelineState).components
            .filter(({ type }) => type !== action.artifactType)
        }

      case REORDER_COMPONENT_IN_CART: {
        const { components } = (state as CustomPipelineState)
        const targetIndex = components.findIndex(({ id }) => id === action.id)
        const target = components.splice(targetIndex, 1)

        return {
          ...state,
          components: components.slice(0, action.position)
            .concat(target, components.slice(action.position, components.length))
        }
      }

      default:
        return state
    }
  }
}

export default reducer
export { initial as CustomPipelineInitial }
