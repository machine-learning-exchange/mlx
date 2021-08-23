import * as React from 'react';
import ReactMarkdown from 'react-markdown'
import remarkToc from 'remark-toc'

export default class MarkdownViewer extends React.Component<{url: string}, {terms: any}> {
    constructor(props: any) {
      super(props)
  
      this.state = { terms: null }
    }
  
    componentWillMount() {
      fetch(this.props.url).then((response) => response.text()).then((text) => {
        this.setState({ terms: text })
      })
    }
  
    render() {
      return (
        <div className="content">
          <ReactMarkdown source={this.state.terms} plugins={[remarkToc]}/>
        </div>
      )
    }
  }