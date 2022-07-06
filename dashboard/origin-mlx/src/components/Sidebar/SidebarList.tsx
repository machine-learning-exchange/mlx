/*
* Copyright 2021 The MLX Contributors
*
* SPDX-License-Identifier: Apache-2.0
*/
import React, { useContext, useEffect, useState } from 'react';
import Icon from '@material-ui/core/Icon';
import { Link } from 'react-router-dom';
import StoreContext from '../../lib/stores/context';
import SidebarHeader from './SideBarHeader';
import SidebarListItem from './SidebarListItem';
import '../../styles/Sidebar.css';
import SecretMenu from '../SecretMenu';
import { capitalize, getUserInfo, hasRole } from '../../lib/util';

const sideNavColors = {
  bg: '#303030',
  fgActive: '#fff',
  fgActiveInvisible: 'rgb(227, 233, 237, 0)',
  fgDefault: '#666',
  hover: '#3f3f3f',
  separator: '#666',
};

const isAdmin = hasRole(getUserInfo(), 'admin');

function getWindowDimensions() {
  const { innerWidth: width, innerHeight: height } = window;
  return {
    width,
    height,
  };
}

function useWindowDimensions() {
  const [windowDimensions, setWindowDimensions] = useState(getWindowDimensions());

  useEffect(() => {
    function handleResize() {
      setWindowDimensions(getWindowDimensions());
    }

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return windowDimensions;
}

function SidebarList() {
  const { store } = useContext(StoreContext);
  const { settings, pages } = store;
  const { active } = pages;
  const { execute } = settings.capabilities;

  const enabled = (artifact: string): boolean => {
    const setting = settings.artifacts[artifact];
    return setting.value !== undefined ? setting.value : setting.default;
  };

  const artifacts = Object.keys(store.settings.artifacts).filter(enabled).filter((artifact: string) => artifact !== 'workspace' && artifact !== 'operators');
  const [secretVisible, setSecretVisible] = useState(false);
  const { height } = useWindowDimensions();
  // Ensures the "Join the Conversation" button is away from the other buttons (if there is enough space)
  const buffer = !isAdmin ? (height - 600) : (height - 670) / 2; // checks if you are an admin , spacing for guardHeight will change such that elements are placed at the bottom
  const guardHeight = height > 700 && !secretVisible ? buffer : 0;

  console.log(height);

  return (
    <div className="sidebar-container">
      <div
        style={{
          textAlign: 'left',
          color: sideNavColors.fgActive,
          backgroundColor: sideNavColors.bg,
          height: '100%',
        }}
      >
        <SidebarHeader
          name="Home"
          active={active === 'home'}
        />
        {artifacts
          && (
          <ul className="sidebar-list">
            <SidebarListItem
              key="Home"
              name="Home"
              icon="home"
              active={active === 'home'}
            />
            {artifacts
              .filter((type) => type !== 'workspace')
              .map((type) => (
                <SidebarListItem
                  key={type}
                  icon={(iconMap as any)[type]}
                  name={type === 'inferenceservices' ? 'KFServices' : capitalize(type)}
                  active={type === active}
                />
              ))}
            {(execute.value !== undefined ? execute.value : execute.default)
              && artifacts.includes('workspace')
              && (
              <SidebarListItem
                icon="code"
                name="Workspace"
                active={active === 'Workspace'}
              />
              )}
            <div style={{ height: guardHeight }} />
            <li className="sidebar-list-wrap">
              <Link to="/external-links">
                <h3 className={`sidebar-list-item ${false ? 'active' : 'not-active'}`}>
                  <div style={{ display: 'flex' }}>
                    <div style={{ paddingRight: 5, verticalAlign: 'middle' }}>
                      <Icon className="sidebar-icon" style={{ marginTop: 7 }}>chat</Icon>
                    </div>
                    <div>
                      <text>Join the Conversation</text>
                    </div>
                  </div>
                </h3>
              </Link>
            </li>
          </ul>
          )}
        <div className="bottom-sidebar">
          { isAdmin && (secretVisible
            ? (
              <div className="secret-tab-open" onClick={() => setSecretVisible(false)}>
                <SecretMenu />
              </div>
            )
            : (
              <div className="secret-tab sidebar-list-wrap" onClick={() => setSecretVisible(true)}>
                <div className="display-secret-menu-button sidebar-list-item">
                  <Icon>settings</Icon>
                  <h3 className="secret-title">Settings</h3>
                </div>
              </div>
            )
          )}
        </div>
      </div>
    </div>
  );
}

export default SidebarList;

const iconMap = {
  pipelines: 'device_hub',
  components: 'developer_boards',
  models: 'layers',
  notebooks: 'library_books',
  operators: 'donut_large',
  datasets: 'storage',
  workspace: 'code',
  inferenceservices: 'layers',
};
