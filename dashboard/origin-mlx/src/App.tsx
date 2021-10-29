/*
* Copyright 2021 The MLX Contributors
*
* SPDX-License-Identifier: Apache-2.0
*/
import React, { Dispatch, useEffect } from 'react';
import reducer, { initial } from './lib/stores/reducer';
import StoreContext, { Store } from './lib/stores/context';
import { Action, State } from './lib/stores/types';
import { GET_SETTINGS } from './lib/stores/settings';
import { findInvalidCacheEntries } from './lib/api/artifacts';
import { getSettings } from './lib/api/settings';
import { getUserInfo, hasRole } from './lib/util';

import TagManager from 'react-gtm-module';

import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import PipelineDetail from './components/Detail/PipelineDetail';
import DatasetDetail from './components/Detail/DatasetDetail';
import ComponentDetail from './components/Detail/ComponentDetail';
import ModelDetail from './components/Detail/ModelDetail';
import NotebookDetail from './components/Detail/NotebookDetail';
import KFServingDetail from './components/Detail/KFServingDetail';
import './App.css';

import { SettingsPage } from './pages/SettingsPage';
import LandingPage from './pages/LandingPage'
import ExternalLinksPage from './pages/ExternalLinksPage'
import MetaDeletePage from './pages/MetaDeletePage';
import MetaFeaturedPage from './pages/MetaFeaturedPage';
import KFServingFeaturedPage from './pages/KFServingFeaturedPage';
import KFServingAllPage from './pages/KFServingAllPage';
import KFServingDetailPage from './pages/KFServingDetailPage';
import KFServingUploadPage from './pages/KFServingUploadPage';
import MetaAllPage from './pages/MetaAllPage';
import UploadPage from './pages/UploadPage';
import MetaDetailPage from './pages/MetaDetailPage';
import IframePage from './pages/IframePage';
import Default404Page from './pages/Default404Page';

// initialize Google Analytics (Google Tag Manager)
if (process.env.REACT_APP_GTM_ID) {
  console.log("Google Analytics is enabled.");
  const tagManagerArgs = {
      gtmId: process.env.REACT_APP_GTM_ID
  }
  TagManager.initialize(tagManagerArgs);
}

const isAdmin = hasRole(getUserInfo(), 'admin');

function App() {

  var prefix = process.env.REACT_APP_BASE_PATH || ""

  // Removes the stored path if the user navigated away from the /experiments page
  if (!window.location.pathname.substring(0, prefix.length+12).includes(prefix + "/experiments"))
    localStorage.removeItem("experiments-iframe")

  // receive iframe message when iframe is loaded and send correct namespace back.
  window.addEventListener('message', (event: MessageEvent) => {
    const { data, origin } = event;
    switch (data.type) {
    case 'iframe-connected':
      ['iframe', 'iframe-run'].forEach((id) => {
        const element = document.getElementById(id) as HTMLIFrameElement;
        if (element) {
          // TODO: get namespace from user info, use fixed value: mlx for now
          element.contentWindow.postMessage({type: 'namespace-selected', value: 'mlx'}, origin);
        }
      })
      break;
    }
  });

  // Removes any invalid cache entries after enough time has passed since the last invalid check
  useEffect(() => {
    findInvalidCacheEntries()
  })

  return (
    <div className="app-wrapper">
      <Store
        reducer={reducer}
        initial={initial}
        onLoaded={({ settings }: State, d: Dispatch<Action>) => {
          const { api } = settings.endpoints
          const API = api.value || api.default
          getSettings(`${API}/apis/v1alpha1`)
            .then(settings => d({ type: GET_SETTINGS, settings }))
            .catch(error => console.log("Failed to reach API: ", API))
        }}
      >
        <StoreContext.Consumer>
          {({ store }) => {
            const { settings } = store

            const { api, kfp } = settings.endpoints
            const API = api.value || api.default
            const KFP = kfp.value || kfp.default

            const { execute } = settings.capabilities
            const canRun = execute.value !== undefined ? execute.value : execute.default

            const switchProps : AppRouterSwitchProps = {
              API, KFP, canRun
            }

            return (
              <Router basename={process.env.REACT_APP_BASE_PATH}>
                <Sidebar>
                  {AppRouterSwitch(switchProps)}
                </Sidebar>
              </Router>
            )
          }}
        </StoreContext.Consumer>
      </Store>
    </div>
  )
}

interface AppRouterSwitchProps {
  API: string,
  KFP: string,
  canRun: boolean
}

function AppRouterSwitch(props: AppRouterSwitchProps) {
  const {API, KFP, canRun} = props

  return (
    <Switch>
      <Route exact path="/" component={LandingPage} />
      <Route exact path="/external-links" component={ExternalLinksPage} />
      <Route exact path="/pipelines"
        render={routeProps =>
          <MetaFeaturedPage
            assetType="pipelines"
            description="Pipelines for your machine learning workloads."
            hasAssets
            alternateBG
            leftBtn="View all Pipelines"
            leftLink="/pipelines/all"
            leftAdmin={true}
            rightBtn="Register a Pipeline"
            rightLink="/upload/pipelines"
            rightAdmin={true}
          />
        }
      />
      <Route exact path="/datasets"
        render={routeProps =>
          <MetaFeaturedPage
            assetType="datasets"
            description="Datasets for your machine learning workloads."
            hasAssets
            alternateBG
            leftBtn="View all Datasets"
            leftLink="/datasets/all"
            leftAdmin={true}
            rightBtn="Register a Dataset"
            rightLink="/upload/datasets"
            rightAdmin={true}
          />
        }
      />
      <Route exact path="/components"
        render={ routeProps =>
          <MetaFeaturedPage
            { ...routeProps }
            assetType="components"
            description="Components that can be used to build your pipelines."
            hasAssets
            leftBtn="View all Components"
            leftLink="/components/all"
            leftAdmin={true}
            rightBtn="Register a Component"
            rightLink="/upload/components"
            rightAdmin={true}
          />
        }
      />
      <Route exact path="/models"
        render={ routeProps =>
          <MetaFeaturedPage
            { ...routeProps }
            assetType="models"
            description="Machine learning models that can be used in your pipelines."
            runningStatus=""
            statusIcon=""
            alternateBG
            hasAssets
            leftBtn="View all Models"
            leftLink="/models/all"
            leftAdmin={true}
            rightBtn="Register a Model"
            rightLink="/upload/models"
            rightAdmin={true}
          />
        }
      />
      <Route exact path="/inferenceservices"
        render={ routeProps =>
          <KFServingFeaturedPage
            { ...routeProps }
            assetType="inferenceservices"
            description="KFServing inference services."
            alternateBG
            hasAssets
            leftBtn="View all Services"
            leftLink="/inferenceservices/all"
            leftAdmin={true}
            rightBtn="Deploy a Service"
            rightLink="/upload/inferenceservices"
            rightAdmin={true}
          />
        }
      />
      <Route path="/workspace"
        render={(routeProps) => {
          window.open(`${KFP}/hub/login`, '_blank')
          routeProps.history.goBack()
          return null
        }}
      />
      <Route exact path="/notebooks"
        render={routeProps =>
          <MetaFeaturedPage
            { ...routeProps }
            assetType="notebooks"
            description="Notebooks for your data science tasks."
            leftBtn="View all Notebooks"
            leftLink="/notebooks/all"
            leftAdmin={true}
            rightBtn="Register a Notebook"
            rightLink="upload/notebooks"
            rightAdmin={true}
          />
        }
      />
      <ProtectedRoute exact path="/pipelines/all"
        render={ () =>
          <MetaAllPage
            type="pipelines"
            description="Pipelines for your machine learning workloads."
            tagName="Category"
            getTag={(asset: any) => 'OpenSource'}
            alternateBG
            leftBtn="Featured"
            leftLink="/pipelines"
            leftIcon="arrow_back"
            rightBtn="Register a Pipeline"
            rightLink="/upload/pipelines"
            canEdit={true}
          />
        }
      />
      <ProtectedRoute exact path="/datasets/all"
        render={ () =>
          <MetaAllPage
            type="datasets"
            description="Datasets for your machine learning workloads."
            tagName="Category"
            getTag={(asset: any) => 'OpenSource'}
            alternateBG
            leftBtn="Featured"
            leftLink="/datasets"
            leftIcon="arrow_back"
            rightBtn="Register a Dataset"
            rightLink="/upload/datasets"
            canEdit={true}
          />
        }
      />
      <ProtectedRoute exact path="/components/all"
        render={ () =>
          <MetaAllPage
            type="components"
            description="Components that can be used to build your pipelines."
            tagName="Platform"
            getTag={(asset: any) =>
              asset.metadata?.annotations?.platform
              || 'OpenSource'}
            alternateBG
            leftBtn="Featured"
            leftLink="/components"
            leftIcon="arrow_back"
            rightBtn="Register a Component"
            rightLink="/upload/components"
            canEdit={true}
          />
        }
      />
      <ProtectedRoute exact path="/models/all"
        render={ () =>
          <MetaAllPage
            type="models"
            description="Machine learning models that can be used in your pipelines."
            tagName="Domain"
            getTag={(asset: any) => asset.domain}
            alternateBG
            leftBtn="Featured"
            leftLink="/models"
            leftIcon="arrow_back"
            rightBtn="Register a Model"
            rightLink="/upload/models"
            canEdit={true}
          />
        }
      />
      <ProtectedRoute exact path="/inferenceservices/all"
        render={ () =>
          <KFServingAllPage
            type="inferenceservices"
            description="KFServing inference services."
            runningStatus=""
            statusIcon=""
            tagName="Domain"
            getTag={(asset: any) => asset.domain}
            alternateBG
            leftBtn="Featured"
            leftLink="/inferenceservices"
            leftIcon="arrow_back"
            rightBtn="Deploy a Service"
            rightLink="/upload/inferenceservices"
            rightAdmin={true}
            canEdit={true}
          />
        }
      />
      <ProtectedRoute exact path="/notebooks/all"
        render={ () =>
          <MetaAllPage
            type="notebooks"
            description="Notebooks for your data science tasks."
            tagName="Platform"
            getTag={(asset: any) => asset.metadata?.annotations?.platform || 'OpenSource'}
            alternateBG
            leftBtn="Featured"
            leftLink="/notebooks"
            leftIcon="arrow_back"
            rightBtn="Register a Notebook"
            rightLink="/upload/notebooks"
            canEdit={true}
          />
        }
        />
      <ProtectedRoute
        exact
        path="/experiments"
        render={() =>
          <IframePage
            title="KFP Experiments"
            path={KFP + "/pipeline/#/experiments" + window.location.pathname.substring(window.location.pathname.indexOf("/experiments")+12)}
            storageKey="experiments-iframe"
          />
        }
      />
      <ProtectedRoute
        exact path="/upload/inferenceservices"
        render={() => <KFServingUploadPage/> }
      />
      <ProtectedRoute
        path="/upload/:type"
        render={(routeProps: any) => <UploadPage {...routeProps} /> }
      />
      <ProtectedRoute path="/delete/:type"
        render={(routeProps: any) =>
          <MetaDeletePage
            { ...routeProps }
            API={ API }
            canRun={ canRun }
            alternateBG
          >
          </MetaDeletePage>
        }
      />
      <ProtectedRoute path="/settings" render={(routeProps: any) => <SettingsPage alternateBG />} />
      <Route path="/pipelines/:id"
        render={({ match, location })=> (
          <MetaDetailPage
            type="pipelines"
            id={match.params.id}
            asset={location}
          >
            <PipelineDetail />
          </MetaDetailPage>
        )}
      />
      <Route path="/datasets/:id"
        render={({ match, location })=> (
          <MetaDetailPage
            type="datasets"
            id={match.params.id}
            asset={location}
          >
            <DatasetDetail />
          </MetaDetailPage>
        )}
      />
      <Route path="/components/:id"
        render={({ match, location })=> (
          <MetaDetailPage
            type="components"
            id={match.params.id}
            asset={location}
          >
            <ComponentDetail />
          </MetaDetailPage>
        )}
      />
      <Route path="/models/:id"
        render={({ match, location })=> (
          <MetaDetailPage
            type="models"
            id={match.params.id}
            asset={location}
          >
            <ModelDetail />
          </MetaDetailPage>
        )}
      />
      <Route path="/inferenceservices/:id"
        render={({ match, location })=> (
          <KFServingDetailPage
            type="inferenceservices"
            id={match.params.id}
            asset={location}
          >
            <KFServingDetail />
          </KFServingDetailPage>
        )}
      />
      <Route path="/notebooks/:id"
        render={({ match, location })=> (
          <MetaDetailPage
            type="notebooks"
            id={match.params.id}
            asset={location}
          >
            <NotebookDetail />
          </MetaDetailPage>
        )}
      />
      <Route render={()=><Default404Page/>}/>
    </Switch>
  )
}

interface ProtectedRouteProps {
  exact?: boolean,
  path: string,
  render: any
}
function ProtectedRoute(props: ProtectedRouteProps) {

  return (
    <Route 
      { ...props }
      render={isAdmin 
        ? props.render 
        : () => <Redirect to='/login'></Redirect>
      }
    />
  )
}

export default App;
