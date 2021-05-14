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

import Menu from "@material-ui/core/Menu";
import MenuItem from "@material-ui/core/MenuItem";

interface SidebarListItemProps {
  name: string;
  icon: string;
  active: string;
}

interface ExpandableItemProps {
  title: string;
  link: string;
  icon: string;
  active: string;
  items: {
    name: string;
    link: string;
    icon: string;
  }[]
}

const SidebarListItem: React.FunctionComponent<SidebarListItemProps> = (props) => {
  const { active: isActive } = props
  var link = props.name.toLocaleLowerCase();

  const pipelinesExpandable: ExpandableItemProps = {
    title: "Pipelines",
    link: "pipelines",
    icon:"device_hub", 
    active: props.active,
    items: [
      {name: "Pipelines", link:"/pipelines", icon:"device_hub"},
      {name: "Components", link:"/components", icon:"developer_boards"}
    ]
  };

  const modelsExpandable: ExpandableItemProps = {
    title: "Models",
    link: "models",
    icon:"layers", 
    active: props.active,
    items: [
      {name: "Registered Models", link:"/models", icon:"layers"},
      {name: "Deployed Models", link:"/inferenceservices", icon:"layers"}
    ]
  };

  if (props.name === 'Pipelines') {
    link = 'pipelines'
    return (
      ExpandableItem(pipelinesExpandable)
    )

  }
  else if (props.name === 'Components') {
    link = 'components'
    return (
      <></>
    );
  }
  else if (props.name === 'Models') {
    link = 'models'
    return (
      ExpandableItem(modelsExpandable)
    )
  }
  else if (props.name === 'KFServices') {
    link = 'inferenceservices'
    return (
      <></>
    );
  }
  else if (props.name === "Datasets") {
    link = 'datasets'
  }
  else if (props.name === 'Notebooks') {
    link = 'notebooks'
  }
  else if (props.name === 'Operators') {
    link = 'operators'
  }
  else if (props.name === 'Workspace') {
    link = 'workspace'
  }
  else {
    link = 'inferenceservices'
  }
  
  return (
    <li className="sidebar-list-wrap">
      <Link to={`/${link}`}>
        <h3 className={`sidebar-list-item ${isActive === link ? 'active' : 'not-active'}`}>
          <Icon className="sidebar-icon">{props.icon}</Icon>
          {props.name}
        </h3>
      </Link>
    </li>
  );
};

function ExpandableItem(props: ExpandableItemProps) {

  const [anchorEl, setAnchorEl] = React.useState(null);
  function handleClick(event: any) {
    if (anchorEl !== event.currentTarget) {
      setAnchorEl(event.currentTarget);
    }
  }

  function handleClose() {
    setAnchorEl(null);
  }

  // Prevents using the <Link> route while still using the same styling
  function cancelClick(event: any) {
    event.preventDefault();
  }

  return (
    <li className="sidebar-list-wrap">
      <div
        aria-owns={anchorEl ? "simple-menu" : undefined}
        aria-haspopup="true"
        onClick={handleClick}
      >
        <Link to={`/static`} onClick={cancelClick}>
          <h3 className={`sidebar-list-item ${props.active === props.link ? 'active' : 'not-active'}`}>
            <Icon className="sidebar-icon">{props.icon}</Icon>
            {props.title}
          </h3>
        </Link>
      </div>
      <Menu
        id="simple-menu"
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleClose}
        MenuListProps={{ onMouseLeave: handleClose }}
      >
        {
          props.items.map((item) => {
            return (
              <MenuItem 
                className={`expandable-list-menu ${'/'+props.active === item.link ? 'active' : 'not-active'}`} 
                onClick={handleClose}
              >
                <Link className={"inherit-color"} to={item.link}>
                  <h3 className={"inherit-color"} /*className={`expandable-list-item ${'/'+props.active === item.link ? 'active' : 'not-active'}`}*/>
                    <Icon className="sidebar-icon">{item.icon}</Icon>
                    {item.name}
                  </h3>
                </Link>
              </MenuItem>
            )
          })
        }
      </Menu>
    </li>
  )
}

export default SidebarListItem;
