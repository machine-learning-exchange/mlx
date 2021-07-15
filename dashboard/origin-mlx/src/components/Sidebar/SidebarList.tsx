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
import React, { useContext, useState } from 'react';
import StoreContext from '../../lib/stores/context'
import SidebarHeader from './SideBarHeader';
import SidebarListItem from './SidebarListItem';
import '../../styles/Sidebar.css'
import Icon from '@material-ui/core/Icon';
import SecretMenu from '../SecretMenu';
import { capitalize, getUserInfo, hasRole } from '../../lib/util';
import { Link } from 'react-router-dom';

const sideNavColors = {
  bg: '#303030',
  fgActive: '#fff',
  fgActiveInvisible: 'rgb(227, 233, 237, 0)',
  fgDefault: '#666',
  hover: '#3f3f3f',
  separator: '#666',
};

const isAdmin = hasRole(getUserInfo(), 'admin');

function SidebarList() {
  const { store } = useContext(StoreContext)
  const { settings, pages } = store
  const { active } = pages
  const { execute } = settings.capabilities

  const enabled = (artifact: string): boolean => {
    const setting = settings.artifacts[artifact]
    return setting.value !== undefined ? setting.value : setting.default
  }

  const artifacts = Object.keys(store.settings.artifacts).filter(enabled).filter((artifact: string) => {return artifact !== "workspace" && artifact !== "operators"})
  const [secretVisible, setSecretVisible] = useState(false)

  return (
    <div className="sidebar-container">
      <div 
        style={{
          "textAlign": "left",
          "color": sideNavColors.fgActive,
          "backgroundColor": sideNavColors.bg, 
      }}>
        <SidebarHeader 
          name="Home"
          active={active === 'home'}
        />
        {artifacts && 
          <ul className="sidebar-list">
            <SidebarListItem
              key={"Home"}
              name={"Home"}
              icon={"home"}
              active={active === 'home'}
            />
            {artifacts
              .filter(type => type !== "workspace")
              .map(type => 
                <SidebarListItem 
                  key={type}
                  icon={(iconMap as any)[type]}
                  name={type === 'inferenceservices' ? 'KFServices' : capitalize(type)}
                  active={type === active}
                />
              )
            }
            {(execute.value !== undefined ? execute.value : execute.default)
              && artifacts.includes('workspace') &&
              <SidebarListItem 
                icon="code"
                name="Workspace"
                active={'Workspace' === active}
              />
            }
          </ul>
        }
      </div>
      <div className="bottom-sidebar">
        <div className={"sidebar-list-wrap footer-list-wrap" + (!secretVisible ? " conversation-margin" : "")}>
          <Link to="/external-links">
            <h3 className={`sidebar-list-item footer-list-item ${false ? 'active' : 'not-active'}`}>
              <Icon className="sidebar-icon">chat</Icon>
              Join the Conversation
            </h3>
          </Link>
        </div>
        { !secretVisible &&
          <div className="secret-divider"></div>
        }
        { isAdmin && (secretVisible ?
            <div className="secret-tab-open" onClick={() => setSecretVisible(false)}>
              <SecretMenu/>
            </div>
          :
            <div className="secret-tab" onClick={() => setSecretVisible(true)}>
              <Icon>more_horiz</Icon>
            </div>
        )}
      </div>
    </div>
  )
}

export default SidebarList

const iconMap = {
  pipelines: "device_hub",
  components: "developer_boards",
  models: "layers",
  notebooks: "library_books",
  operators: "donut_large",
  datasets: "storage",
  workspace: "code",
  inferenceservices: "layers"
}
