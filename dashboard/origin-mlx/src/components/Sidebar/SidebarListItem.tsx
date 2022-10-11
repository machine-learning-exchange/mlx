/*
* Copyright 2021 The MLX Contributors
*
* SPDX-License-Identifier: Apache-2.0
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
  const { active: isActive } = props;
  let link = props.name.toLocaleLowerCase();

  if (props.name === 'Pipelines') {
    link = 'pipelines';
  } else if (props.name === 'Datasets') {
    link = 'datasets';
  } else if (props.name === 'Components') {
    link = 'components';
  } else if (props.name === 'Models') {
    link = 'models';
  } else if (props.name === 'Notebooks') {
    link = 'notebooks';
  } else if (props.name === 'Operators') {
    link = 'operators';
  } else if (props.name === 'KFServices') {
    link = 'inferenceservices';
  } else if (props.name === 'Workspace') {
    link = 'workspace';
  } else if (props.name === 'Home') {
    link = '';
  } else {
    link = 'inferenceservices';
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
