/*
* Copyright 2021 The MLX Contributors
*
* SPDX-License-Identifier: Apache-2.0
*/
import * as React from 'react';
import { UnControlled as CodeMirror } from 'react-codemirror2';

require('codemirror/lib/codemirror.css');
require('codemirror/theme/yeti.css');
require('codemirror/theme/solarized.css');
require('codemirror/theme/neo.css');
require('codemirror/mode/xml/xml');
require('codemirror/mode/javascript/javascript');
require('codemirror/mode/yaml/yaml');
require('codemirror/mode/python/python');
require('codemirror/addon/display/autorefresh');

interface SourceCodeDisplayProps {
  code: string;
  isYAML: boolean;
  scrollMe?: boolean;
}

const SourceCodeDisplay: React.FunctionComponent<SourceCodeDisplayProps> = (props) => (
  <div className="code-content-wrapper">
    <div className="code-content-wrapper">
      { props.code.length
        ? (
          <div className="code-wrapper">
            <CodeMirror
              cursor={{
                line: 50,
                ch: 0,
              }}
              className="source-code"
              value={props.code}
              options={{
                theme: 'neo',
                mode: props.isYAML ? 'yaml' : 'python',
                lineNumbers: false,
                readOnly: 'true',
                width: '100%',
                lineWrapping: true,
                autorefresh: true,
                autoScroll: true,
              }}
            />
          </div>
        )
        : <p>loading source code...</p>}
    </div>
  </div>
);

export default SourceCodeDisplay;
