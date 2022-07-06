/*
* Copyright 2021 The MLX Contributors
*
* SPDX-License-Identifier: Apache-2.0
*/
import React from 'react';
import MLXLogo from '../../images/mlx-logo-name-white.png';
import Link from '../Link';
import LFAILogo from '../../images/lfaidata.png';

interface SideBarHeaderProps {
  name: string;
  active: boolean;
}

const SideBarHeader: React.FunctionComponent<SideBarHeaderProps> = (props) => (
  <div className="sidebar-header-wrap">
    <Link to="/">
      <img alt="MLX Logo" className="sidebar-img" src={MLXLogo} />
    </Link>
    <hr className="sidebar-divider" />
    <Link to="https://lfaidata.foundation/">
      <img alt="LFAI Logo" className="lfai-logo above-secret" src={LFAILogo} />
    </Link>
  </div>
);

export default SideBarHeader;
