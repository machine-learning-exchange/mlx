/* 
* Copyright 2021 IBM Corporation
* 
* SPDX-License-Identifier: Apache-2.0
*/ 
import React from 'react'
import MaterialButton from '@material-ui/core/Button'


function Button(props: any) {
  return (<MaterialButton {...props}>{props.children}</MaterialButton>)
}

export default Button
