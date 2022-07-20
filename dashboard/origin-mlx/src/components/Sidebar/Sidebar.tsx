/*
* Copyright 2021 The MLX Contributors
*
* SPDX-License-Identifier: Apache-2.0
*/
import React, { ReactNode } from 'react';
import ReactSidebar from 'react-sidebar';
import SidebarList from './SidebarList';

const sideNavColors = {
  bg: '#303030',
  fgActive: '#fff',
  fgActiveInvisible: 'rgb(227, 233, 237, 0)',
  fgDefault: '#666',
  hover: '#3f3f3f',
  separator: '#666',
};

function Sidebar(props: { children: ReactNode }) {
  return (
    <ReactSidebar
      sidebar={<SidebarList />}
      open
      docked
      styles={{
        sidebar: {
          color: sideNavColors.fgActive,
          backgroundColor: sideNavColors.bg,
          width: '240px',
          height: '100%',
          overflow: 'hidden auto',
        },
      }}
    >
      {props.children}
    </ReactSidebar>
  );
}

export default Sidebar;
