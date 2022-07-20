/*
* Copyright 2021 The MLX Contributors
*
* SPDX-License-Identifier: Apache-2.0
*/
import React, { useState } from 'react';
import styled from 'styled-components';

function ToolTip(props: any) {
  const { content, children } = props;
  const [isShown, setIsShown] = useState(false);

  return (
    <Wrapper
      onMouseEnter={(event: never) => setIsShown(true)}
      onMouseLeave={(event: never) => setIsShown(false)}
    >
      {children}
      <Display enabled={isShown}>{content}</Display>
    </Wrapper>
  );
}

const Display = styled.div<{ enabled?: boolean }>`
  visibility: ${({ enabled }) => (enabled ? 'visible' : 'hidden')};
  opacity: ${({ enabled }) => (enabled ? 1 : 0)};

  position: absolute;
  left: calc(100% + 10px);
  top: 50%;
  transform: translateY(-50%);

  width: 200px;
  padding: 15px;
  border-radius: 5px;
  border: 1px solid #fff;
  z-index: 3;

  background-color: ${({ theme }) => theme.bg};
  transition: visibility 250ms linear, opacity 250ms linear;
  color: ${({ theme }) => theme.fgActive};
`;

Display.defaultProps = {
  theme: {
    bg: '#303030',
    fgActive: '#fff',
    fgActiveInvisible: 'rgb(227, 233, 237, 0)',
    fgDefault: '#666',
    hover: '#3f3f3f',
    separator: '#666',
  },
};

const Wrapper = styled.div`
  position: relative;
`;

export default ToolTip;
