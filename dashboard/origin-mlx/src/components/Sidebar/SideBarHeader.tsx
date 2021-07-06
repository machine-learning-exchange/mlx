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
import React from 'react'
import MLXLogo from "../../images/mlx-logo-name-white.png";
import Link from '../Link'
import LFAILogo from "../../images/lfaidata.png";

interface SideBarHeaderProps {
  name: string;
  active: boolean;
}

const SideBarHeader: React.FunctionComponent<SideBarHeaderProps> = (props) => {  
  return (
    <div className="sidebar-header-wrap">
      <Link to="/">
        <img alt="MLX Logo" className="sidebar-img" src={MLXLogo} />
      </Link>
      <hr className="sidebar-divider"/>
      <Link to="https://lfaidata.foundation/"> 
        <img alt="LFAI Logo" className="lfai-logo above-secret" src={LFAILogo} /> 
      </Link> 
    </div>
  );
};

export default SideBarHeader;
