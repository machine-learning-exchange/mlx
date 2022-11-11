/*
* Copyright 2021 The MLX Contributors
*
* SPDX-License-Identifier: Apache-2.0
*/
import * as React from 'react';
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import rehypeSlug from 'rehype-slug'
import assert from "assert"

export default class MarkdownViewer extends React.Component<{url: string}, {terms: any}> {
  constructor(props: any) {
    super(props)

    this.state = { terms: null }
  }

  UNSAFE_componentWillMount() {
    let url = this.props.url
    let headers: {[index: string]: any} = {}

    if (url.includes("github") && !url.includes("raw")) {
      // convert plain GitHub url to "raw" url
      url = this.props.url.replace("/blob/", "/")
        .replace("/github.ibm.com/", "/raw.github.ibm.com/")
        .replace("/github.com/", "/raw.githubusercontent.com/")
    }

    if (url.includes("github.ibm.com")) {
      // for Enterprise GitHub we use the GitHub API (v3) and a (read-only) API token
      // https://docs.github.com/en/enterprise-server@3.1/rest/repos/contents#get-contents
      // when using a personal access token the minimal set of permission required
      // are 'repo' and 'admin:org/read:org' (on a private repository)
      //
      // i.e.:
      //   readme_url: https://github.ibm.com/CODAIT/MAX-Age-Estimation/blob/master/README.md
      //
      // curl -H 'Authorization: token ${REACT_APP_GHE_API_TOKEN}' \
      //   -H 'Accept: application/vnd.github.v3.raw' \
      //   -L https://github.ibm.com/api/v3/repos/CODAIT/MAX-Age-Estimation/contents/README.md

      const url_segments = url.split(/[#?]+/)[0].split("/")
      assert(url_segments[0] === "https:")
      let api_base = "https://github.ibm.com/api/v3"
      let owner = url_segments[3]
      let repo = url_segments[4]
      let ref = url_segments[5]
      let path = url_segments.slice(6).join("/")
      url = `${api_base}/repos/${owner}/${repo}/contents/${path}?ref=${ref}`

      const ghe_api_token = process.env.REACT_APP_GHE_API_TOKEN
      if (!ghe_api_token) {
        console.log("Enterprise GitHub API Token must be provided via env var REACT_APP_GHE_API_TOKEN.")
      }
      headers["Authorization"] = `token ${ghe_api_token}`
      headers["Accept"] = "application/vnd.github.v3.raw"
    }
    fetch(url, {
      headers: headers
    }).then((response) => response.text()).then((text) => {
      this.setState({ terms: text })
    })
  }
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
