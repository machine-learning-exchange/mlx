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
import React, { useState } from 'react'
import styled from 'styled-components'

function ToolTip(props: any) {
  const { content, children } = props;
  const [ isShown, setIsShown ] = useState(false)

  return (
    <Wrapper
      onMouseEnter={(event: never) => setIsShown(true)}
      onMouseLeave={(event: never) => setIsShown(false)}
    >
      {children}
      <Display enabled={isShown}>{content}</Display>
    </Wrapper>
  )
}


const Display = styled.div<{ enabled?: boolean }>`
  visibility: ${ ({ enabled }) => enabled ? 'visible' : 'hidden' };
  opacity: ${ ({ enabled }) => enabled ? 1 : 0 };

  position: absolute;
  left: calc(100% + 10px);
  top: 50%;
  transform: translateY(-50%);

  width: 200px;
  padding: 15px;
  border-radius: 5px;
  border: 1px solid #fff;
  z-index: 3;

  background-color: ${ ({ theme }) => theme.bg };
  transition: visibility 250ms linear, opacity 250ms linear;
  color: ${ ({ theme }) => theme.fgActive };
`

Display.defaultProps = {
  theme: {
    bg: '#303030',
    fgActive: '#fff',
    fgActiveInvisible: 'rgb(227, 233, 237, 0)',
    fgDefault: '#666',
    hover: '#3f3f3f',
    separator: '#666',
  }
}

const Wrapper = styled.div`
  position: relative;
`


export default ToolTip
