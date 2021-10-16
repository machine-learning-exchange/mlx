/* 
* Copyright 2021 The MLX Contributors
* 
* SPDX-License-Identifier: Apache-2.0
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
