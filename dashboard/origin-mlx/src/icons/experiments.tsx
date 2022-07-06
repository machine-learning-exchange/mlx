/*
 * Copyright 2018 kubeflow.org
 *
 * SPDX-License-Identifier: Apache-2.0
 */

import * as React from 'react';

export default class ExperimentsIcon extends React.Component<{ color: string }> {
  public render(): JSX.Element {
    return (
      <svg width="20" height="20" viewBox="0 0 20 12" xmlns="http://www.w3.org/2000/svg">
        <g id="Symbols" fill="none" fillRule="evenodd">
          <g transform="translate(-26 -72)">
            <g transform="translate(0 12)">
              <g transform="translate(0 44)">
                <g id="Group-3">
                  <g transform="translate(26 12)">
                    <polygon points="0 0 20 0 20 20 0 20" />
                    <path
                      d="M15,5.83333333 L13.825,4.65833333 L8.54166667,9.94166667
                      L9.71666667,11.1166667 L15,5.83333333 Z M18.5333333,4.65833333
                      L9.71666667,13.475 L6.23333333,10 L5.05833333,11.175 L9.71666667,15.8333333
                      L19.7166667,5.83333333 L18.5333333,4.65833333 Z M0.341666667,11.175
                      L5,15.8333333 L6.175,14.6583333 L1.525,10 L0.341666667,11.175 Z"
                      fill={this.props.color}
                      fillRule="nonzero"
                    />
                  </g>
                </g>
              </g>
            </g>
          </g>
        </g>
      </svg>
    );
  }
}
