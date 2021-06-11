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
import React, { Dispatch } from 'react';
import reducer, { initial } from './lib/stores/reducer'
import StoreContext, { Store } from './lib/stores/context'
import { Action, State } from './lib/stores/types'
import { GET_SETTINGS } from './lib/stores/settings';
import { getSettings } from './lib/api/settings';
import { getUserInfo, hasRole } from './lib/util'

import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import PipelineDetail from './components/Detail/PipelineDetail';
import DatasetDetail from './components/Detail/DatasetDetail';
import ComponentDetail from './components/Detail/ComponentDetail';
import ModelDetail from './components/Detail/ModelDetail';
import OperatorDetail from './components/Detail/OperatorDetail';
import NotebookDetail from './components/Detail/NotebookDetail';
import KFServingDetail from './components/Detail/KFServingDetail';
import './App.css';

import { SettingsPage } from './pages/SettingsPage';
import LandingPage from './pages/LandingPage'
import MetaDeletePage from './pages/MetaDeletePage';
import MetaFeaturedPage from './pages/MetaFeaturedPage';
import KFServingFeaturedPage from './pages/KFServingFeaturedPage';
import KFServingAllPage from './pages/KFServingAllPage';
import KFServingDetailPage from './pages/KFServingDetailPage';
import KFServingUploadPage from './pages/KFServingUploadPage';
import MetaAllPage from './pages/MetaAllPage';
import UploadPage from './pages/UploadPage'
import MetaDetailPage from './pages/MetaDetailPage';
import IframePage from './pages/IframePage'

const isAdmin = hasRole(getUserInfo(), 'admin');

function App() {

  var prefix = process.env.REACT_APP_BASE_PATH || ""

  // Removes the stored path if the user navigated away from the /experiments page
  if (!window.location.pathname.substring(0, prefix.length+12).includes(prefix + "/experiments"))
    localStorage.removeItem("experiments-iframe")

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

            return (
              <Router basename={process.env.REACT_APP_BASE_PATH}>
                <Sidebar>
                  <Route exact path="/" component={LandingPage} />
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
                  <Switch>
                    { isAdmin &&
                    <Route path="/pipelines/all"
                      render={ routeProps =>
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
                    }
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
                  </Switch>
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
                  <Switch>
                    { isAdmin &&
                    <Route path="/datasets/all"
                      render={ routeProps =>
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
                    }
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
                  </Switch>
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
                  <Switch>
                  { isAdmin &&
                    <Route path="/components/all"
                      render={ routeProps =>
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
                    }
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
                  </Switch>
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
                  <Switch>
                  { isAdmin &&
                    <Route path="/models/all"
                      render={ routeProps =>
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
                    }
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
                  </Switch>
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
                  <Switch>
                    <Route path="/inferenceservices/all"
                      render={ routeProps =>
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
                  </Switch>
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
                  <Switch>
                  { isAdmin &&
                    <Route path="/notebooks/all"
                      render={ routeProps =>
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
                    }
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
                  </Switch>
                  <Route exact path="/operators"
                    render={ routeProps =>
                      <MetaFeaturedPage
                        { ...routeProps }
                        hasAssets
                        assetType="operators"
                        description="Operators for your machine learning stack."
                        leftBtn="View all Operators"
                        leftLink="/operators/all"
                        leftAdmin={true}
                        rightBtn="Register an Operator"
                        rightLink="/upload/operators"
                        rightAdmin={true}
                      />
                    }
                  />
                  <Switch>
                    { isAdmin &&
                    <Route path="/operators/all"
                      render={ routeProps =>
                        <MetaAllPage
                          type="operators"
                          description="Operators for your machine learning stack."
                          tagName="Categories"
                          getTag={(asset: any) => asset.metadata?.annotations?.categories || 'AI/Machine Learning'}
                          alternateBG
                          leftBtn="Featured"
                          leftLink="/operators"
                          leftIcon="arrow_back"
                          rightBtn="Register an Operator"
                          rightLink="/upload/operators"
                          canEdit={true}
                        />
                      }
                    />
                    }
                    <Route path="/operators/:id"
                      render={({ match, location })=> (
                        <MetaDetailPage
                          type="operators"
                          id={match.params.id}
                          asset={location}
                        >
                          <OperatorDetail />
                        </MetaDetailPage>
                      )}
                    />
                  </Switch>
                  { isAdmin &&
                  <Route
                    path="/experiments"
                    render={({match, location}) =>
                      <IframePage
                        title="KFP Experiments"
                        path={KFP + "/_/pipeline/?ns=mlx#/experiments" + window.location.pathname.substring(window.location.pathname.indexOf("/experiments")+12)}
                        storageKey="experiments-iframe"
                      />
                    }
                  />
                  }
                  { isAdmin &&
                  <Switch>
                    <Route
                      exact path="/upload/inferenceservices"
                      render={routeProps => <KFServingUploadPage {...routeProps} /> }
                    />
                    <Route
                      path="/upload/:type"
                      render={routeProps => <UploadPage {...routeProps} /> }
                    />
                  </Switch>
                  }
                  { isAdmin &&
                  <Route path="/delete/:type"
                  render={routeProps =>
                    <MetaDeletePage
                    { ...routeProps }
                    API={ API }
                    canRun={ canRun }
                    alternateBG>
                      </MetaDeletePage>
                    }
                    />
                  }
                  { isAdmin &&
                  <Route path="/settings" render={routeProps => <SettingsPage alternateBG />} />
                  }
                </Sidebar>
              </Router>
            )
          }}
        </StoreContext.Consumer>
      </Store>
    </div>
  )
}

export default App;
