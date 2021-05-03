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
import * as React from 'react';
import { Typography } from '@material-ui/core';
import styled from 'styled-components';

import Logo from '../icons/codaitLogo'
import Rotate from './Rotate'

export interface ILoadingMessageProps {
  assetType?: string
  message?: string
}

const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
  flex: 1;
  width: 100%;
  align-items: center;
  justify-content: center;
`;

export default function LoadingMessage (props: ILoadingMessageProps) {
  const { assetType, message } = props
  return (
    <Wrapper>
      <Rotate period="5s"><Logo color="#fff" style={{}}/></Rotate>
      <Typography variant="subtitle1">
        {assetType && `loading ${assetType} metadata...`}
        {message && message}
      </Typography>
    </Wrapper>
  );
}
