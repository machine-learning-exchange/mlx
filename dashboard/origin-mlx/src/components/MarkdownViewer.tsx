/*
* Copyright 2021 The MLX Contributors
*
* SPDX-License-Identifier: Apache-2.0
*/
import * as React from 'react';
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import rehypeSlug from 'rehype-slug'

export default class MarkdownViewer extends React.Component<{url: string}, {terms: any}> {
  constructor(props: any) {
    super(props)

    this.state = { terms: null }
  }

  UNSAFE_componentWillMount() {
    // use a UI server API endpoint `/readme` to request README.md files from
    // GitHub Enterprise, to not expose API tokens on the client web browser
    fetch(`/readme?url=${encodeURIComponent(this.props.url)}`)
      .then(response => response.text())
      .then((text) => {
        this.setState({terms: text})
      })
  };

  render() {
    return (
      <div className="content">
        <ReactMarkdown children={this.state.terms}
                       remarkPlugins={[remarkGfm]}
                       rehypePlugins={[rehypeSlug]}/>
      </div>
    )
  }
}
