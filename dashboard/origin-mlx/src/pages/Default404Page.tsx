/*
* Copyright 2021 The MLX Contributors
*
* SPDX-License-Identifier: Apache-2.0
*/
import React, { useContext } from 'react';
import StoreContext from '../lib/stores/context';
import Hero from '../components/Hero';
import { SET_ACTIVE_PAGE } from '../lib/stores/pages';

export default function Default404Page() {
  const { store, dispatch } = useContext(StoreContext);
  const { active } = store.pages;

  if (active !== 'home') dispatch({ type: SET_ACTIVE_PAGE, page: 'home' });

  return (
    <div className="landing-page">
      <Hero
        title="Machine Learning Exchange"
        subtitle=" "
      />
      <div className="default-404-page-wrapper">
        <h1 className="default-404-page-text">404</h1>
        <h2 className="default-404-page-text">Sorry, we couldn&#39;t find that page.</h2>
      </div>
    </div>
  );
}
