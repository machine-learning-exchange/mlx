/*
 * Copyright 2018 kubeflow.org
 *
 * SPDX-License-Identifier: Apache-2.0
 */

import createMuiTheme from '@material-ui/core/styles/createMuiTheme';
import { NestedCSSProperties } from 'typestyle/lib/types';
import { style, stylesheet } from 'typestyle';

// tslint:disable:object-literal-sort-keys
export const zIndex = {
  DROP_ZONE_OVERLAY: 1,
  GRAPH_NODE: 1,
  BUSY_OVERLAY: 2,
  PIPELINE_SUMMARY_CARD: 2,
  SIDE_PANEL: 2,
};

export const color = {
  activeBg: '#eaf1fd',
  alert: '#f9ab00', // Google yellow 600
  background: '#fff',
  blue: '#4285f4', // Google blue 500
  disabledBg: '#666',
  divider: '#e0e0e0',
  errorBg: '#FBE9E7',
  errorText: '#D50000',
  foreground: '#000',
  graphBg: '#f5f5f5',
  grey: '#5f6368', // Google grey 500
  hoverBg: '#eee',
  inactive: '#5F6368',
  lightGrey: '#eee', // Google grey 200
  lowContrast: '#80868b', // Google grey 600
  secondaryText: 'rgba(0, 0, 0, .88)',
  separator: '#e8e8e8',
  strong: '#212121',
  success: '#34a853',
  terminated: '#80868b',
  theme: '#666',
  themeDarker: '#3f3f3f',
  warningBg: '#f9f9e1',
  weak: '#9AA0A6',
};

export const dimension = {
  auto: 'auto',
  base: 40,
  jumbo: 64,
  large: 48,
  small: 36,
  tiny: 24,
  xlarge: 56,
  xsmall: 32,
};

const baseSpacing = 24;
export const spacing = {
  base: baseSpacing,
  units: (unit: number) => baseSpacing + unit * 4,
};

export const fonts = {
  code: '"Source Code Pro", monospace',
  main: '"Google Sans", "Helvetica Neue", sans-serif',
  secondary: '"Roboto", "Helvetica Neue", sans-serif',
};

export const fontsize = {
  base: 14,
  large: 18,
  medium: 16,
  small: 12,
  title: 18,
};

const palette = {
  primary: {
    dark: color.themeDarker,
    main: color.theme,
  },
  secondary: {
    main: 'rgba(0, 0, 0, .38)',
  },
};

export const theme = createMuiTheme({
  overrides: {
    MuiButton: {
      flat: {
        fontSize: fontsize.base,
        fontWeight: 'bold',
        minHeight: dimension.tiny,
        textTransform: 'none',
      },
      flatPrimary: {
        border: '1px solid #ddd',
        cursor: 'pointer',
        fontSize: fontsize.base,
        marginRight: 10,
        textTransform: 'none',
      },
      flatSecondary: {
        color: color.theme,
      },
      root: {
        '&$disabled': {
          backgroundColor: 'initial',
        },
        color: color.theme,
        marginRight: 10,
        padding: '0 8px',
      },
    },
    MuiDialogActions: {
      root: {
        margin: 15,
      },
    },
    MuiDialogTitle: {
      root: {
        fontSize: fontsize.large,
      },
    },
    MuiFormControlLabel: {
      root: {
        marginLeft: 0,
      },
    },
    MuiFormLabel: {
      filled: {
        marginLeft: 0,
        marginTop: 0,
      },
      root: {
        '&$focused': {
          marginLeft: 0,
          marginTop: 0,
        },
        fontSize: fontsize.base,
        marginLeft: 5,
        marginTop: -8,
      },
    },
    MuiIconButton: {
      root: {
        padding: 9,
      },
    },
    MuiInput: {
      input: { padding: 0 },
      root: { padding: 0 },
    },
    MuiInputAdornment: {
      positionEnd: {
        paddingRight: 0,
      },
      root: { padding: 0 },
    },
    MuiTooltip: {
      tooltip: {
        backgroundColor: '#666',
        color: '#f1f1f1',
        fontSize: 12,
      },
    },
  },
  palette,
  typography: {
    fontFamily: fonts.main,
    fontSize: `${fontsize.base} !important` as any,
    useNextVariants: true,
  },
});

export const commonCss = stylesheet({
  absoluteCenter: {
    left: 'calc(50% - 15px)',
    position: 'absolute',
    top: 'calc(50% - 15px)',
  },
  busyOverlay: {
    backgroundColor: '#ffffffaa',
    bottom: 0,
    left: 0,
    position: 'absolute',
    right: 0,
    top: 0,
    zIndex: 1,
  },
  buttonAction: {
    $nest: {
      '&:disabled': {
        backgroundColor: color.background,
      },
      '&:hover': {
        backgroundColor: theme.palette.primary.dark,
      },
    },
    backgroundColor: palette.primary.main,
    color: 'white',
  },
  ellipsis: {
    display: 'block',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    whiteSpace: 'nowrap',
  },
  flex: {
    alignItems: 'center !important',
    display: 'flex !important',
    flexShrink: 0,
  },
  flexColumn: {
    display: 'flex !important',
    flexDirection: 'column',
  },
  flexGrow: {
    display: 'flex !important',
    flexGrow: 1,
  },
  header: {
    fontSize: fontsize.large,
    fontWeight: 'bold',
    paddingBottom: 16,
    paddingTop: 20,
  },
  ibmCard: {
    backgroundColor: '#525252',
    borderRadius: '7px',
    fontFamily: 'Helvetica Neue, Arial, sans-serif',
    height: '100%',
    marginBottom: '10px',
    width: '20%',
    boxShadow: '0 2px 4px rgba(0,0,0,0.16), 0 2px 4px rgba(0,0,0,0.23)',
    $nest: {
      '&:hover': {
        boxShadow: '0 6px 12px rgba(0,0,0,0.25), 0 6px 12px rgba(0,0,0,0.43)',
      },
    },
  },

  ibmCardBackGround: {
    backgroundColor: '#525252',
    fontFamily: 'Helvetica Neue, Arial, sans-serif',
    borderRadius: '7px',
    padding: '10px 10px 0px 10px',
    // TODO: need to change to adjust to ibmCard's height automatically
    position: 'relative',
    verticalAlign: 'top',
    height: '15vw',
    width: '15vw',
    boxShadow: '0 2px 4px rgba(0,0,0,0.16), 0 2px 4px rgba(0,0,0,0.23)',
    $nest: {
      '&:hover': {
        boxShadow: '0 6px 12px rgba(0,0,0,0.25), 0 6px 12px rgba(0,0,0,0.43)',
      },
    },
    overflow: 'hidden',
  },
  ibmCardBottom: {
    bottom: '0px',
    padding: '0 0 10px 0',
    backgroundColor: '#525252',
    position: 'absolute',
    width: '15vw',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-end',
  },

  ibmCardDescription: {
    color: '#fff',
    margin: '10px 0 0 0',
  },

  ibmCardLink: {
    textDecoration: 'none',
  },

  ibmTable: {
    padding: '5px',
    borderSpacing: '30px',
  },

  ibmTag: {
    alignItems: 'center',
    border: '1px solid #b0b0b0',
    borderRadius: '.93rem',
    display: 'inline-flex',
    fontFamily: 'ibm-plex-sans, Helvetica Neue, Arial, sans-serif',
    padding: '.18rem .4rem',
    whiteSpace: 'nowrap',
    maxWidth: '85%',
    textOverflow: 'ellipsis',
  },

  infoIcon: {
    color: color.lowContrast,
    height: 16,
    width: 16,
  },
  link: {
    $nest: {
      '&:hover': {
        color: color.theme,
        textDecoration: 'underline',
      },
    },
    color: color.strong,
    cursor: 'pointer',
    textDecoration: 'none',
  },
  noShrink: {
    flexShrink: 0,
  },
  page: {
    display: 'flex',
    flexFlow: 'column',
    flexGrow: 1,
    overflow: 'auto',
  },
  pageOverflowHidden: {
    display: 'flex',
    flexFlow: 'column',
    flexGrow: 1,
    overflowX: 'auto',
    overflowY: 'hidden',
  },
  prewrap: {
    whiteSpace: 'pre-wrap',
  },
  scrollContainer: {
    background:
      `linear-gradient(white 30%, rgba(255,255,255,0)),
       linear-gradient(rgba(255,255,255,0), white 70%) 0 100%,
       radial-gradient(farthest-corner at 50% 0, rgba(0,0,0,.2), rgba(0,0,0,0)),
       radial-gradient(farthest-corner at 50% 100%, rgba(0,0,0,.2), rgba(0,0,0,0)) 0 100%`,
    backgroundAttachment: 'local, local, scroll, scroll',
    backgroundColor: 'white',
    backgroundRepeat: 'no-repeat',
    backgroundSize: '100% 40px, 100% 40px, 100% 2px, 100% 2px',
    overflow: 'auto',
    position: 'relative',
  },
  textField: {
    display: 'flex',
    height: 40,
    marginBottom: 20,
    marginTop: 15,
  },
  unstyled: {
    color: 'inherit',
    outline: 'none',
    textDecoration: 'none',
  },
});

export function _paddingInternal(units?: number, directions?: string): NestedCSSProperties {
  units = units || baseSpacing;
  directions = directions || 'blrt';
  const rules: NestedCSSProperties = {};
  if (directions.indexOf('b') > -1) {
    rules.paddingBottom = units;
  }
  if (directions.indexOf('l') > -1) {
    rules.paddingLeft = units;
  }
  if (directions.indexOf('r') > -1) {
    rules.paddingRight = units;
  }
  if (directions.indexOf('t') > -1) {
    rules.paddingTop = units;
  }
  return rules;
}

export function padding(units?: number, directions?: string): string {
  return style(_paddingInternal(units, directions));
}
