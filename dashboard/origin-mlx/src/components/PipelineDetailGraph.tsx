/* 
* Copyright 2021 The MLX Contributors
* 
* SPDX-License-Identifier: Apache-2.0
*/ 
import * as React from 'react';
import '../styles/Graph.css';
import dagre from 'dagre';

const NODE_WIDTH = 150;
const NODE_HEIGHT = 70;
const CANVAS_WIDTH = 800;
const CANVAS_HEIGHT = 640;
const CANVAS_X_PAD = 100;
const CANVAS_Y_PAD = 60;
const MAX_LABEL_LENGTH = 17;
const LABEL_X_OFFSET = 10;

export interface IPipelineDetailGraphProps {
  selectedNode: string;
  entrypoint: string
  templates: Array<any>;
  handleClick: Function;
}

export default class PipelineDetailGraph extends React.Component<IPipelineDetailGraphProps, any> {
  canvas: any;
  setRef: (element: any) => void;
  constructor(props:IPipelineDetailGraphProps) {
    super(props);
    this.canvas = null;

    this.setRef = element => {
      this.canvas = element;
    };
    this.state = {
      graphWidth: 0,
      graphHeight: 0,
      nodeRects: [],
      hoverNode: '',
      activeNode: '',
      hoverState: false,
      selectedNode: props.selectedNode
    }
  }

  componentDidMount() {    
    let canvas = this.canvas as HTMLCanvasElement;
    const ctx = canvas.getContext('2d');
    const graph = this.buildGraph(this.props.entrypoint, this.props.templates);
    const { graphWidth, graphHeight } = this.getGraphDims(graph)
    canvas.width = graphWidth + CANVAS_X_PAD
    canvas.height = graphHeight + CANVAS_Y_PAD

    // DRAW NODES
    let nodeList:any = [];
    graph.nodes().forEach((name: string) => {
      const node = graph.node(name)

      ctx.lineWidth = 1.5;
      ctx.strokeStyle = "slategray"; 
      ctx.fillStyle = "#ddd";
      ctx.font = "12px Arial";

      const label = node.label
      const labelWidth = Math.round(ctx.measureText(label).width);

      let nodeRect = {
        x: node.x - (NODE_WIDTH / 2),
        y: node.y - (NODE_HEIGHT / 2),
        width: NODE_WIDTH,
        height: NODE_HEIGHT,
        label
      }

      // const extraPadPerSide = (nodeRect.width - labelWidth - LABEL_X_OFFSET) / 2;

      ctx.fillRect(nodeRect.x, nodeRect.y, nodeRect.width, nodeRect.height);
      ctx.strokeRect(nodeRect.x, nodeRect.y, nodeRect.width, nodeRect.height);
      ctx.fillStyle = "black";
      ctx.fillText(label, node.x - (NODE_WIDTH / 2) + LABEL_X_OFFSET, node.y);
      nodeList.push(nodeRect)
    })

    this.setState({
      nodeRects: nodeList
    })
    
    // DRAW EDGES
    graph.edges().forEach(function(e:any) {
      const edge = graph.edge(e);
      //console.log("Edge " + e.v + " -> " + e.w + ": " + JSON.stringify(edge));
      ctx.strokeStyle = "lightslategray";
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.lineJoin = 'bevel';

      const [ start, ...rest ] = edge.points
      ctx.moveTo(start.x, start.y)
      rest.forEach((point: any) => ctx.lineTo(point.x, point.y))
      ctx.stroke();

      const lastBegin = edge.points[edge.points.length - 2]
      const lastEnd = edge.points[edge.points.length - 1]

      arrow(ctx, lastBegin, lastEnd, 7)
    });

    // working on interactivity / hover action
    canvas.onmousemove = ((e:any) => {
      let rect = canvas.getBoundingClientRect(),
        mouseX = e.clientX - rect.left,
        mouseY = e.clientY - rect.top,
        i = 0, r;
      // console.log({x, y})
      this.state.nodeRects.forEach((rect:any, i:number) => {
        if (this.inRect(mouseX, mouseY, rect)) {
          this.highlightNode(i, 'hover');
        } else if (this.props.selectedNode === rect.label) {
          this.highlightNode(i, 'selected')
        } else {
          this.highlightNode(i, 'none');
        }
      })
    })

    canvas.onclick = ((e: any) => {
      let rect = canvas.getBoundingClientRect(),
        mouseX = e.clientX - rect.left,
        mouseY = e.clientY - rect.top,
        i = 0, r;
      // console.log({x, y})
      this.state.nodeRects.forEach((rect:any, i:number) => {
        if (this.inRect(mouseX, mouseY, rect)) {
          this.props.handleClick(rect.label)
          return
        } 
      })
    })

    canvas.onchange = (e:any) => {
      console.log(this.props.selectedNode)
    }
  }

  inRect = (mouseX: number, mouseY: number, rect: any) =>
    (mouseX >= rect.x && mouseX <= rect.x+rect.width) && (mouseY >= rect.y && mouseY <= rect.y+rect.height)

  highlightNode = (nodeID: number, state: string) => {
    const node = this.state.nodeRects[nodeID];
    let canvas = this.canvas as HTMLCanvasElement;
    const ctx = canvas.getContext('2d');
    
    ctx.lineWidth = 1.5; 
    if (state === 'hover') {
      ctx.strokeStyle = "turquoise"; 
    } else if (state === 'selected') {
      ctx.strokeStyle = 'darkturquoise';
    } else {
      ctx.strokeStyle = 'lightslategray';
    }
    ctx.strokeRect(node.x, node.y, node.width, node.height);
  }

  getGraphDims = (graph:any) => {
    const xs = Object.values(graph._nodes).map((node:any) => node.x)
    const graphXMax = Math.max(...xs) + (0.5 * NODE_WIDTH)
    const graphXMin = Math.min(...xs) - (0.5 * NODE_WIDTH)

    const ys = Object.values(graph._nodes).map((node:any) => node.y)
    const graphYMax = Math.max(...ys) + (0.5 * NODE_HEIGHT)
    const graphYMin = Math.min(...ys) - (0.5 * NODE_HEIGHT)

    return {
      graphWidth: graphXMax - graphXMin,
      graphHeight: graphYMax - graphYMin
    }
  }

  buildGraph = (entrypoint: string, templates: any[]) => {
    const dagNodes = this.props.templates.filter((t:any) => {
      return t.hasOwnProperty('dag')
    })  

    let nonDagNodes = this.props.templates.filter((t:any) => {
      return !t.hasOwnProperty('dag')
    }).map(node=>node.name)
    
    // create a new directed graph
    const g = new dagre.graphlib.Graph()
      .setGraph({})
      .setDefaultEdgeLabel(function() { return {}; });

    if (dagNodes) {
      dagNodes.forEach((node:any) => {
        node.dag.tasks.forEach((task:any) => {
          // shorten long labels
          const label = task.name.length > MAX_LABEL_LENGTH ?
            task.name.substring(0, MAX_LABEL_LENGTH) + '...' : task.name

          if (task.hasOwnProperty('dependencies')) {
            // add node
            g.setNode(task.name, { label, width: NODE_WIDTH, height: NODE_HEIGHT });
            nonDagNodes.push(task.name)

            // add edges
            task.dependencies.forEach((dep:any) => {
              g.setEdge(dep, task.name);
            })
          } else {
            g.setNode(task.name, { label, width: NODE_WIDTH, height: NODE_HEIGHT });            
          }
        })
      })

      // catch deeper dependencies
      dagNodes.forEach((node:any) => {
        node.dag.tasks.forEach((task:any) => {
          if (task.hasOwnProperty('arguments') && node.hasOwnProperty('name')) {
            const target = node.dag.tasks.filter((t:any) => !t.hasOwnProperty('dependencies'))
            if (g.nodes().includes(target[0].template) && nonDagNodes.includes(node.name)) {
              g.setEdge(node.name, target[0].template)
              console.log(`${node.name} connects to ${target[0].template}`)
            }
          }
        })
      })
    }
    dagre.layout(g);
    return g;
  }
  
  public render() {
  return (
      <>
        <div className="canvas-wrap">
          <canvas 
            ref={ this.setRef }
            width={ String(CANVAS_WIDTH) }
            height={ String(CANVAS_HEIGHT) }
            className="graph-canvas"
          />
        </div>
      </>
    );
  }
}

function arrow (ctx: any, p1: any, p2: any, size: number) {
  var angle = Math.atan2((p2.y - p1.y) , (p2.x - p1.x));
  var hyp = Math.sqrt((p2.x - p1.x) * (p2.x - p1.x) + (p2.y - p1.y) * (p2.y - p1.y));

  ctx.save();
  ctx.translate(p1.x, p1.y);
  ctx.rotate(angle);

  // line
  ctx.beginPath();	
  ctx.moveTo(0, 0);
  ctx.lineTo(hyp - size, 0);
  ctx.stroke();

  // triangle
  ctx.fillStyle = '#4d4d4d';
  ctx.beginPath();
  ctx.lineTo(hyp - size, size);
  ctx.lineTo(hyp, 0);
  ctx.lineTo(hyp - size, -size);
  ctx.fill();

  ctx.restore();
}
