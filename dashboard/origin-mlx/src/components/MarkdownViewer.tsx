import * as React from 'react';
import ReactMarkdown from 'react-markdown'

export default class MarkdownViewer extends React.Component<{}, {terms: any}> {
    constructor(props: any) {
      super(props)
  
      this.state = { terms: null }
    }
  
    componentWillMount() {
      fetch("https://raw.githubusercontent.com/IBM/MAX-Object-Detector/master/README.md").then((response) => response.text()).then((text) => {
        this.setState({ terms: text })
      })
    }
  
    render() {
      return (
        <div className="content">
          <ReactMarkdown source={this.state.terms} />
        </div>
      )
    }
  }