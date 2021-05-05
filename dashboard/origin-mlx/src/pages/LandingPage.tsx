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
import introPic from "../images/landing-page.png";
import { SET_ACTIVE_PAGE } from '../lib/stores/pages';

export default function LandingPage() {
  const { store, dispatch } = useContext(StoreContext)
  const { branding } = store.settings
  const { active } = store.pages

  const name = branding.name.value || branding.name.default

  if (active !== 'home')
    dispatch({ type: SET_ACTIVE_PAGE, page: 'home' })

  return (
    <div className="landing-page">
      <Hero
        title={name} 
        subtitle=" "
      >
      </Hero>
      <div className="landing-page-wrapper">
        <h2 className="landing-page-text"> &nbsp;&nbsp;&nbsp;MLX - Data and AI Assets Catalog and Execution Engine</h2>
        <img alt="MLX View" className="slide-img" src={introPic} />
      </div>
    </div>
  );
}
