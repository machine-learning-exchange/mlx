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
