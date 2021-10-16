/* 
* Copyright 2021 The MLX Contributors
* 
* SPDX-License-Identifier: Apache-2.0
*/ 
import React from 'react'
import Button from './Button'
import Tooltip from '../Tooltip/Tooltip'


function ButtonWithTooltip(props: any) {
  const { tooltip, children, ...rest } = props

  return (
    <Tooltip content={tooltip}>
      <Button {...rest}>
        {children}
      </Button>
    </Tooltip>
  )
}

export default ButtonWithTooltip
