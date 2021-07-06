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
import React, { useContext } from 'react';
import StoreContext from '../lib/stores/context'
import Hero from '../components/Hero'
import { SET_ACTIVE_PAGE } from '../lib/stores/pages';
import Link from '../components/Link'
import PageFooter from '../components/PageFooter';
import Paper from '@material-ui/core/Paper'

export default function LandingPage() {
  const { store, dispatch } = useContext(StoreContext)
  const { active } = store.pages

  if (active !== 'external-links')
    dispatch({ type: SET_ACTIVE_PAGE, page: 'external-links' })

  return (
    <div className="links-page">
      <Hero
        title={"Join the Conversation"} 
        subtitle=" "
      >
      </Hero>
      <div className="upload-wrapper">
        <Paper className="upload-form-wrapper">
        <h3 className="links-page-text">
          Slack: <Link to="https://lfaifoundation.slack.com/archives/C0264LKNH63"> ml-exchange </Link>
          <br/> 
          Github: <Link to="https://github.com/machine-learning-exchange"> Machine Learning eXchange (MLX) </Link> 
        </h3>
        </Paper>
      </div>
      <PageFooter/>
    </div>
  );
}