/*
 * Copyright 2019 kubeflow.org
 *
 * SPDX-License-Identifier: Apache-2.0
 */

import * as React from 'react';
import { CSSProperties } from 'jss/css';
export default class StatusRunning extends React.Component<{ style: CSSProperties }> {
  public render(): JSX.Element {
    const { style } = this.props;
    return (
      <svg width={style.width as string} height={style.height as string} viewBox='0 0 18 18'>
        <g stroke='none' strokeWidth='1' fill='none' fillRule='evenodd'>
          <g transform='translate(-1.000000, -1.000000)'>
            <polygon points='0 0 18 0 18 18 0 18' />
            <path
              d='M8.9925,1.5 C4.8525,1.5 1.5,4.86 1.5,9 C1.5,13.14 4.8525,16.5 8.9925,16.5
              C13.14,16.5 16.5,13.14 16.5,9 C16.5,4.86 13.14,1.5 8.9925,1.5 Z M9,15 C5.685,15
              3,12.315 3,9 C3,5.685 5.685,3 9,3 C12.315,3 15,5.685 15,9 C15,12.315 12.315,15 9,15 Z'
              fill={style.color as string}
              fillRule='nonzero'
            />
            <polygon fill={style.color as string} fillRule='nonzero' points='6 6 12 6 12 12 6 12' />
          </g>
        </g>
      </svg>
    );
  }
}
