/* 
* Copyright 2021 The MLX Contributors
* 
* SPDX-License-Identifier: Apache-2.0
*/ 
import React, { ReactNode } from 'react'
import { capitalize } from '../lib/util'

import DataList from './DataList'


interface MetadataViewProps {
  content: {
    [name: string]: (any | ReactNode)[]
  },
  titleIcon?: JSX.Element
}

function MetadataView(props: MetadataViewProps) {
  const { content } = props

  return (
    <div style={{ overflow: 'none', height: 'auto', padding: '0.5rem' }}>
      {Object.entries(content).filter(([_, value]) => !!value).map(([ name, data ]) => (
        <DataList
          key={name}
          title={`${capitalize(name)}`}
          titleIcon={props.titleIcon}
          items={data.filter(item => !!item).map(field => React.isValidElement(field)
            ? field
            : {
              ...field,
              data: field.description || field.data,
              defaultData: field.default
            }
          )}
        />
      ))}
    </div>
  )
}

export default MetadataView
