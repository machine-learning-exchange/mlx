/*
 * Copyright 2018 kubeflow.org
 *
 * SPDX-License-Identifier: Apache-2.0
 */

import { spacing, _paddingInternal } from './Css';
import * as Css from './Css';

describe('Css', () => {
  describe('padding', () => {
    it('returns padding units in all directions by default', () => {
      expect(_paddingInternal()).toEqual({
        paddingBottom: spacing.base,
        paddingLeft: spacing.base,
        paddingRight: spacing.base,
        paddingTop: spacing.base,
      });
    });

    it('returns specified padding units in all directions', () => {
      expect(_paddingInternal(100)).toEqual({
        paddingBottom: 100,
        paddingLeft: 100,
        paddingRight: 100,
        paddingTop: 100,
      });
    });

    it('returns default units in specified directions', () => {
      expect(_paddingInternal(undefined, 'lr')).toEqual({
        paddingLeft: spacing.base,
        paddingRight: spacing.base,
      });
    });

    it('calls internal padding with the same arguments', () => {
      const spy = jest.spyOn(Css, 'padding');
      Css.padding(123, 'abcdefg');
      expect(spy).toHaveBeenCalledWith(123, 'abcdefg');
    });
  });
});
