/*
* Copyright 2021 The MLX Contributors
*
* SPDX-License-Identifier: Apache-2.0
*/
import * as React from 'react';
import { Typography } from '@material-ui/core';
import styled from 'styled-components';

import Logo from '../icons/codaitLogo';
import Rotate from './Rotate';

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

export default function LoadingMessage(props: ILoadingMessageProps) {
  const { assetType, message } = props;
  return (
    <Wrapper>
      <Rotate period="5s"><Logo color="#fff" style={{}} /></Rotate>
      <Typography variant="subtitle1">
        {assetType && `loading ${assetType} metadata...`}
        {message && message}
      </Typography>
    </Wrapper>
  );
}
