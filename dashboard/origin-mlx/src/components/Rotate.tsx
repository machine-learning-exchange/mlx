/*
* Copyright 2021 The MLX Contributors
*
* SPDX-License-Identifier: Apache-2.0
*/
import styled, { keyframes } from 'styled-components';

const rotate = keyframes`
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
`;

interface RotateProps {
  readonly period: string
}

const Rotate = styled.div<RotateProps>`
  display: inline-block;
  animation: ${rotate} ${(props) => props.period} linear infinite;
  vertical-align: middle;
  flex-shrink: 0;
  clip-path: circle(40px at center);
`;

export default Rotate;
