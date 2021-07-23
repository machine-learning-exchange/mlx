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

export default function Default404Page() {
  const { store, dispatch } = useContext(StoreContext)
  const { active } = store.pages

  if (active !== 'home')
    dispatch({ type: SET_ACTIVE_PAGE, page: 'home' })

  return (
    <div className="landing-page">
      <Hero
        title="Machine Learning Exchange"
        subtitle=" "
      >
      </Hero>
      <div className="default-404-page-wrapper">
        <h1 className="default-404-page-text">404</h1>
        <h2 className="default-404-page-text">Sorry, we couldn't find that page.</h2>
      </div>
    </div>
  );
}
