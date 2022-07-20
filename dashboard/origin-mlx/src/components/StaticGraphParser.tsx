/*
 * Copyright 2018-2019 Google LLC
 *
 * SPDX-License-Identifier: Apache-2.0
 */

import * as dagre from 'dagre';
import { color } from '../Css';

export const Constants = {
  NODE_HEIGHT: 64,
  NODE_WIDTH: 172,
};

export type nodeType = 'container' | 'resource' | 'dag' | 'unknown';

export interface KeyValue<T> extends Array<any> {
  0?: string;
  1?: T;
}

export class SelectedNodeInfo {
  public args: string[];

  public command: string[];

  public condition: string;

  public image: string;

  public inputs: Array<KeyValue<string>>;

  public nodeType: nodeType;

  public outputs: Array<KeyValue<string>>;

  public volumeMounts: Array<KeyValue<string>>;

  public resource: Array<KeyValue<string>>;

  constructor() {
    this.args = [];
    this.command = [];
    this.condition = '';
    this.image = '';
    this.inputs = [[]];
    this.nodeType = 'unknown';
    this.outputs = [[]];
    this.volumeMounts = [[]];
    this.resource = [[]];
  }
}

export function _populateInfoFromTask(info: SelectedNodeInfo, task?: any): SelectedNodeInfo {
  if (!task) {
    return info;
  }

  info.nodeType = 'container';
  if (task.taskSpec && task.taskSpec.steps) {
    const { steps } = task.taskSpec;
    info.args = steps[0].args || [];
    info.command = steps[0].command || [];
    info.image = steps[0].image || [];
    info.volumeMounts = (steps[0].volumeMounts || []).map((volume: any) => [
      volume.mountPath,
      volume.name,
    ]);
  }

  if (task.taskSpec && task.taskSpec.params) info.inputs = (task.taskSpec.params || []).map((p: any) => [p.name, p.value || '']);
  if (task.taskSpec.results) info.outputs = (task.taskSpec.results || []).map((p: any) => [p.name, p.description || '']);

  return info;
}

export function createGraph(workflow: any): dagre.graphlib.Graph {
  const graph = new dagre.graphlib.Graph();
  graph.setGraph({});
  graph.setDefaultEdgeLabel(() => ({}));

  buildTektonDag(graph, workflow);
  return graph;
}

function buildTektonDag(graph: dagre.graphlib.Graph, template: any): void {
  const pipeline = template;
  const tasks = (pipeline.spec.pipelineSpec.tasks || []).concat(
    pipeline.spec.pipelineSpec.finally || [],
  );

  const exitHandlers = (pipeline.spec.pipelineSpec.finally || []).map((element: any) => element.name) || [];

  for (const task of tasks) {
    const taskName = task.name;

    // Checks for dependencies mentioned in the runAfter section of a task and then checks for dependencies based
    // on task output being passed in as parameters
    if (task.runAfter) {
      task.runAfter.forEach((depTask: any) => {
        graph.setEdge(depTask, taskName);
      });
    }

    // Adds any dependencies that arise from Conditions and tracks these dependencies to make sure they aren't duplicated in the case that
    // the Condition and the base task use output from the same dependency
    for (const condition of task.conditions || []) {
      for (const condParam of condition.params || []) {
        if (
          condParam.value.substring(0, 8) === '$(tasks.'
          && condParam.value.substring(condParam.value.length - 1) === ')'
        ) {
          const paramSplit = condParam.value.split('.');
          const parentTask = paramSplit[1];

          graph.setEdge(parentTask, taskName);
        }
      }
    }

    for (const param of task.params || []) {
      if (
        param.value.substring(0, 8) === '$(tasks.'
        && param.value.substring(param.value.length - 1) === ')'
      ) {
        const paramSplit = param.value.split('.');
        const parentTask = paramSplit[1];
        graph.setEdge(parentTask, taskName);
      }
    }

    // Add the info for this node
    const info = new SelectedNodeInfo();
    _populateInfoFromTask(info, task);

    const label = exitHandlers.includes(task.name) ? `onExit - ${taskName}` : taskName;
    const bgColor = exitHandlers.includes(task.name)
      ? color.lightGrey
      : task.when
        ? 'cornsilk'
        : undefined;

    graph.setNode(taskName, {
      bgColor,
      height: Constants.NODE_HEIGHT,
      info,
      label,
      width: Constants.NODE_WIDTH,
    });
  }
}
