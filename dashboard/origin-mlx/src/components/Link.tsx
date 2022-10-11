/*
* Copyright 2021 The MLX Contributors
*
* SPDX-License-Identifier: Apache-2.0
*/
import React from 'react';
import { Link as RouterLink, LinkProps } from 'react-router-dom';

function Link(props: LinkProps) {
  const destination = props.to.toString();
  const isExternal = /^https?:\/\//.test(destination);

  return isExternal
    ? <a className="external-link" href={destination} {...props}>{props.children}</a>
    : <RouterLink {...props}>{props.children}</RouterLink>;
}

export default Link;
