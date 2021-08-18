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
import ReactSidebar from 'react-sidebar'
import SidebarList from './SidebarList'


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
      sidebar={ <SidebarList /> }
      open={ true }
      docked={ true }
      styles={{
        sidebar:{
          "color": sideNavColors.fgActive,
          "backgroundColor": sideNavColors.bg,
          "width":"230px",
          "overflow":"hidden"
        }
      }}
    >
      {props.children}
    </ReactSidebar>
  )
}

export default Sidebar
