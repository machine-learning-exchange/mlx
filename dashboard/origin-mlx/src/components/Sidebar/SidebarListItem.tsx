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
  active: string;
}

interface ExpandableItemProps {
  title: string;
  link: string;
  icon: string;
  active: string;
  expandableItems: ExpandableItem[]
}

interface ExpandableItem {
  name: string;
  link: string;
  icon: string;
}

const SidebarListItem: React.FunctionComponent<SidebarListItemProps> = (props) => {
  var link = props.name.toLocaleLowerCase();

  const pipelinesExpandable: ExpandableItemProps = {
    title: "Pipelines",
    link: "pipelines",
    icon:"device_hub", 
    active: props.active,
    expandableItems: [
      {name: "Pipelines", link:"pipelines", icon:"device_hub"},
      {name: "Components", link:"components", icon:"developer_boards"}
    ]
  };

  const modelsExpandable: ExpandableItemProps = {
    title: "Models",
    link: "models",
    icon:"layers", 
    active: props.active,
    expandableItems: [
      {name: "Registered Models", link:"models", icon:"layers"},
      {name: "Deployed Models", link:"inferenceservices", icon:"layers"}
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
        <h3 className={`sidebar-list-item ${props.active === link ? 'active' : 'not-active'}`}>
          <Icon className="sidebar-icon">{props.icon}</Icon>
          {props.name}
        </h3>
      </Link>
    </li>
  );
};

function ExpandableItem(props: ExpandableItemProps) {
  const [isClicked, setIsClicked] = React.useState(false);

  const handleExpandClick = (event: React.MouseEvent<HTMLElement>) => {
    event.preventDefault()
    setIsClicked(!isClicked)
  };

  return (
    <li className="sidebar-list-wrap">
      <Link key={`expandable-${props.title}`} to={""} onClick={handleExpandClick}>
        <h3 className={`sidebar-list-item ${isClicked ? 'active' : 'not-active'}`}>
          <Icon className="sidebar-icon">{props.icon}</Icon>
          {props.title}
        </h3>
      </Link>
      { isClicked &&
        props.expandableItems.map((expandableItem: ExpandableItem) => {
          return (
            <Link key={expandableItem.link} to={`/${expandableItem.link}`} className="sidebar-sublist-item">
              <h3 className={`sidebar-list-item ${props.active === expandableItem.link ? 'active' : 'not-active'}`}>
                <Icon className="sidebar-icon">{expandableItem.icon}</Icon>
                {expandableItem.name}
              </h3>
            </Link>
          )
        })
      }
    </li>
  )
}

export default SidebarListItem;
