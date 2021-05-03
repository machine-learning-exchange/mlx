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
import React, {
  createContext,
  ComponentProps,
  Context as ReactContext,
  Dispatch,
  useReducer,
  useState,
  useEffect
} from 'react'
import { State, Action } from './types'


interface StoreProps extends ComponentProps<any> {
  reducer: (s: State, a: Action) => State
  initial?: Object,
  onLoaded?: (s: State, d: Dispatch<Action>) => void
}

const Context: ReactContext<{ store: State, dispatch: Dispatch<Action>} | null> = createContext(null)

export function Store(props: StoreProps) {
  const { children, reducer, initial, onLoaded } = props
  const [ store, dispatch ] = useReducer(reducer, initial || {})
  const [ isLoaded, setLoaded ] = useState(false)

  useEffect(() => {
    if (!isLoaded) {
      setLoaded(true)
      onLoaded && onLoaded(store, dispatch)
    }
  }, [isLoaded, onLoaded, store])

  return (
    <Context.Provider value={{ dispatch, store }}>
      {isLoaded ? children : <></>}
    </Context.Provider>
  )
}

export default Context
