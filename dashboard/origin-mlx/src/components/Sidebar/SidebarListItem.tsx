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
import { Link } from 'react-router-dom';
import Icon from '@material-ui/core/Icon';

interface SidebarListItemProps {
  name: string;
  icon: string;
  active: boolean;
}

const SidebarListItem: React.FunctionComponent<SidebarListItemProps> = (props) => {
  const { active: isActive } = props
  var link = props.name.toLocaleLowerCase();

  if (props.name === 'Pipelines') {
    link = 'pipelines'
  }
  else if (props.name === "Datasets") {
    link = 'datasets'
  }
  else if (props.name === 'Components') {
    link = 'components'
  }
  else if (props.name === 'Models') {
    link = 'models'
  }
  else if (props.name === 'Notebooks') {
    link = 'notebooks'
  }
  else if (props.name === 'Operators') {
    link = 'operators'
  }
  else if (props.name === 'KFServices') {
    link = 'inferenceservices'
  }
  else if (props.name === 'Workspace') {
    link = 'workspace'
  }
  else if (props.name === 'Home') {
    link = ''
  }
  else {
    link = 'inferenceservices'
  }
  
  return (
    <li className="sidebar-list-wrap">
      <Link to={`/${link}`}>
        <h3 className={`sidebar-list-item ${isActive ? 'active' : 'not-active'}`}>
          <Icon className="sidebar-icon">{props.icon}</Icon>
          {props.name}
        </h3>
      </Link>
    </li>
  );
};

export default SidebarListItem;
