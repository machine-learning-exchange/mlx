/*
 * Copyright 2018-2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import * as dagre from 'dagre';
import ErrorIcon from '@material-ui/icons/Error';
import PendingIcon from '@material-ui/icons/Schedule';
import RunningIcon from '../icons/statusRunning';
import SkippedIcon from '@material-ui/icons/SkipNext';
import SuccessIcon from '@material-ui/icons/CheckCircle';
import CachedIcon from '@material-ui/icons/Cached';
import TerminatedIcon from '../icons/statusTerminated';
import Tooltip from '@material-ui/core/Tooltip';
import UnknownIcon from '@material-ui/icons/Help';
import { color } from '../Css';

export function statusToBgColor(status?: NodePhase, nodeMessage?: string): string {
  status = checkIfTerminated(status, nodeMessage);
  switch (status) {
    case NodePhase.ERROR:
    // fall through
    case NodePhase.FAILED:
      return statusBgColors.error;
    case NodePhase.PENDING:
      return statusBgColors.notStarted;
    case NodePhase.TERMINATING:
    // fall through
    case NodePhase.RUNNING:
      return statusBgColors.running;
    case NodePhase.SUCCEEDED:
      return statusBgColors.succeeded;
    case NodePhase.CACHED:
      return statusBgColors.cached;
    case NodePhase.SKIPPED:
    // fall through
    case NodePhase.TERMINATED:
      return statusBgColors.terminatedOrSkipped;
    case NodePhase.UNKNOWN:
    // fall through
    default:
      console.log("Status to background color: status not recognized")
      return statusBgColors.notStarted;
  }
}

export function formatDateString(date: Date | string | undefined): string {
  if (typeof date === 'string') {
    return new Date(date).toLocaleString();
  } else {
    return date ? date.toLocaleString() : '-';
  }
}

export function checkIfTerminated(status?: NodePhase, nodeMessage?: string): NodePhase | undefined {
  // Argo considers terminated runs as having "Failed", so we have to examine the failure message to
  // determine why the run failed.
  if (status === NodePhase.FAILED && nodeMessage === 'terminated') {
    status = NodePhase.TERMINATED;
  }
  return status;
}

export function statusToIcon(
    status?: NodePhase,
    startDate?: Date | string,
    endDate?: Date | string,
    nodeMessage?: string,
  ): JSX.Element {
    status = checkIfTerminated(status, nodeMessage);
    // tslint:disable-next-line:variable-name
    let IconComponent: any = UnknownIcon;
    let iconColor = color.inactive;
    let title = 'Unknown status';
    switch (status) {
      case NodePhase.ERROR:
        IconComponent = ErrorIcon;
        iconColor = color.errorText;
        title = 'Error while running this resource';
        break;
      case NodePhase.FAILED:
        IconComponent = ErrorIcon;
        iconColor = color.errorText;
        title = 'Resource failed to execute';
        break;
      case NodePhase.PENDING:
        IconComponent = PendingIcon;
        iconColor = color.weak;
        title = 'Pending execution';
        break;
      case NodePhase.RUNNING:
        IconComponent = RunningIcon;
        iconColor = color.blue;
        title = 'Running';
        break;
      case NodePhase.TERMINATING:
        IconComponent = RunningIcon;
        iconColor = color.blue;
        title = 'Run is terminating';
        break;
      case NodePhase.SKIPPED:
        IconComponent = SkippedIcon;
        title = 'Execution has been skipped for this resource';
        break;
      case NodePhase.SUCCEEDED:
        IconComponent = SuccessIcon;
        iconColor = color.success;
        title = 'Executed successfully';
        break;
      case NodePhase.COMPLETED:
        IconComponent = SuccessIcon;
        iconColor = color.success;
        title = 'Executed successfully';
        break;
      case NodePhase.CACHED: // This is not argo native, only applies to node.
        IconComponent = CachedIcon;
        iconColor = color.success;
        title = 'Execution was skipped and outputs were taken from cache';
        break;
      case NodePhase.TERMINATED:
        IconComponent = TerminatedIcon;
        iconColor = color.terminated;
        title = 'Run was manually terminated';
        break;
      case NodePhase.PIPELINERUNTIMEOUT:
        IconComponent = ErrorIcon;
        iconColor = color.errorText;
        title = 'Pipeline run timeout';
        break;
      case NodePhase.COULDNTGETCONDITION:
        IconComponent = ErrorIcon;
        iconColor = color.errorText;
        title = 'Could not retrieve the condition';
        break;
      case NodePhase.CONDITIONCHECKFAILED:
        IconComponent = SkippedIcon;
        title = 'Execution has been skipped due to a Condition check failure';
        break;
      case NodePhase.PIPELINERUNCANCELLED:
        IconComponent = TerminatedIcon;
        iconColor = color.terminated;
        title = 'PipelineRun cancelled';
        break;
      case NodePhase.PIPELINERUNCOULDNTCANCEL:
        IconComponent = TerminatedIcon;
        iconColor = color.terminated;
        title = 'PipelineRun could not cancel';
        break;
      case NodePhase.TASKRUNCANCELLED:
        IconComponent = TerminatedIcon;
        iconColor = color.terminated;
        title = 'TaskRun cancelled';
        break;
      case NodePhase.TASKRUNCOULDNTCANCEL:
        IconComponent = TerminatedIcon;
        iconColor = color.terminated;
        title = 'TaskRun could not cancel';
        break;
      case NodePhase.UNKNOWN:
        break;
      default:
        console.log("Status to icon: status not recognized")
    }
    return (
      <Tooltip
        title={
          <div>
            <div>{title}</div>
            {/* These dates may actually be strings, not a Dates due to a bug in swagger's handling of dates */}
            {startDate && <div>Start: {formatDateString(startDate)}</div>}
            {endDate && <div>End: {formatDateString(endDate)}</div>}
          </div>
        }
      >
        <span style={{ height: 18 }}>
          <IconComponent style={{ color: iconColor, height: 18, width: 18 }} />
        </span>
      </Tooltip>
    );
  }

export const Constants = {
    NODE_HEIGHT: 64,
    NODE_WIDTH: 172,
  };

export interface KeyValue<T> extends Array<any> {
    0?: string;
    1?: T;
  }

export const statusBgColors = {
    error: '#fce8e6',
    notStarted: '#f7f7f7',
    running: '#e8f0fe',
    succeeded: '#e6f4ea',
    cached: '#e6f4ea',
    terminatedOrSkipped: '#f1f3f4',
    warning: '#fef7f0',
};

export enum NodePhase {
    ERROR = 'Error',
    FAILED = 'Failed',
    PENDING = 'Pending',
    RUNNING = 'Running',
    SKIPPED = 'Skipped',
    SUCCEEDED = 'Succeeded',
    COMPLETED = 'Completed',
    CACHED = 'Cached',
    TERMINATING = 'Terminating',
    PIPELINERUNTIMEOUT = 'PipelineRunTimeout',
    COULDNTGETCONDITION = 'CouldntGetCondition',
    CONDITIONCHECKFAILED = 'ConditionCheckFailed',
    PIPELINERUNCANCELLED = 'PipelineRunCancelled',
    PIPELINERUNCOULDNTCANCEL = 'PipelineRunCouldntCancel',
    TASKRUNCANCELLED = 'TaskRunCancelled',
    TASKRUNCOULDNTCANCEL = 'TaskRunCouldntCancel',
    TERMINATED = 'Terminated',
    UNKNOWN = 'Unknown',
}

export function statusToPhase(nodeStatus: string | undefined): NodePhase {
    if (!nodeStatus) return 'Unknown' as NodePhase;
    else if (nodeStatus === 'Completed') return 'Succeeded' as NodePhase;
    else if (nodeStatus === 'ConditionCheckFailed') return 'Skipped' as NodePhase;
    else if (nodeStatus === 'CouldntGetCondition') return 'Error' as NodePhase;
    else if (
        nodeStatus === 'PipelineRunCancelled' ||
        nodeStatus === 'PipelineRunCouldntCancel' ||
        nodeStatus === 'TaskRunCancelled' ||
        nodeStatus === 'TaskRunCouldntCancel'
    )
        return 'Terminated' as NodePhase;
    return nodeStatus as NodePhase;
}

export enum StorageService {
  GCS = 'gcs',
  HTTP = 'http',
  HTTPS = 'https',
  MINIO = 'minio',
  S3 = 's3',
}

export interface StoragePath {
  source: StorageService;
  bucket: string;
  key: string;
}

export default class WorkflowParser {
  public static createRuntimeGraph(workflow: any): dagre.graphlib.Graph {
    const graph = new dagre.graphlib.Graph();
    graph.setGraph({});
    graph.setDefaultEdgeLabel(() => ({}));

    // If a run exists but has no status is available yet return an empty graph
    if (
      workflow &&
      workflow.status &&
      (Object.keys(workflow.status).length === 0 || !workflow.status.taskRuns)
    )
      return graph;

    const tasks = (workflow['spec']['pipelineSpec']['tasks'] || []).concat(
      workflow['spec']['pipelineSpec']['finally'] || [],
    );
    const status = workflow['status']['taskRuns'];
    const pipelineParams = workflow['spec']['params'];
    const exitHandlers =
      (workflow['spec']['pipelineSpec']['finally'] || []).map((element: any) => {
        return element['name'];
      }) || [];

    // Create a map from task name to status for every status received
    const statusMap = new Map<string, any>();
    for (const taskRunId of Object.getOwnPropertyNames(status)) {
      status[taskRunId]['taskRunId'] = taskRunId;
      if (status[taskRunId]['status'])
        statusMap.set(status[taskRunId]['pipelineTaskName'], status[taskRunId]);
    }

    for (const task of tasks) {
      // If the task has a status then add it and its edges to the graph
      if (statusMap.get(task['name'])) {
        const conditions = task['conditions'] || [];
        const taskId =
          statusMap.get(task['name']) && statusMap.get(task['name'])!['status']['podName'] !== ''
            ? statusMap.get(task['name'])!['status']['podName']
            : task['name'];
        const edges = this.checkParams(statusMap, pipelineParams, task, '');

        // Add all of this Task's conditional dependencies as Task dependencies
        for (const condition of conditions)
          edges.push(...this.checkParams(statusMap, pipelineParams, condition, taskId));

        if (task['runAfter']) {
          task['runAfter'].forEach((parentTask: any) => {
            if (
              statusMap.get(parentTask) &&
              statusMap.get(parentTask)!['status']['conditions'][0]['type'] === 'Succeeded'
            ) {
              const parentId = statusMap.get(parentTask)!['status']['podName'];
              edges.push({ parent: parentId, child: taskId });
            }
          });
        }

        for (const edge of edges || []) graph.setEdge(edge['parent'], edge['child']);

        const status = this.getStatus(statusMap.get(task['name']));
        const phase = statusToPhase(status);
        const statusColoring = exitHandlers.includes(task['name'])
          ? '#fef7f0'
          : statusToBgColor(phase, '');
        // Add a node for the Task
        graph.setNode(taskId, {
          height: Constants.NODE_HEIGHT,
          icon: statusToIcon(status),
          label: task['name'],
          statusColoring: statusColoring,
          width: Constants.NODE_WIDTH,
        });
      }
    }

    return graph;
  }

  private static checkParams(
    statusMap: Map<string, any>,
    pipelineParams: any,
    component: any,
    ownerTask: string,
  ): { parent: string; child: string }[] {
    const edges: { parent: string; child: string }[] = [];
    const componentId =
      ownerTask !== ''
        ? component['conditionRef']
        : statusMap.get(component['name']) &&
          statusMap.get(component['name'])!['status']['podName'] !== ''
        ? statusMap.get(component['name'])!['status']['podName']
        : component['name'];

    // Adds dependencies from task params
    for (const param of component['params'] || []) {
      let paramValue = param['value'] || '';

      // If the parameters are passed from the pipeline parameters then grab the value from the pipeline parameters
      if (
        param['value'].substring(0, 9) === '$(params.' &&
        param['value'].substring(param['value'].length - 1) === ')'
      ) {
        const paramName = param['value'].substring(9, param['value'].length - 1);
        for (const pipelineParam of pipelineParams)
          if (pipelineParam['name'] === paramName) paramValue = pipelineParam['value'];
      }
      // If the parameters are passed from the parent task's results and the task is completed then grab the resulting values
      else if (
        param['value'].substring(0, 2) === '$(' &&
        param['value'].substring(param['value'].length - 1) === ')'
      ) {
        const paramSplit = param['value'].split('.');
        const parentTask = paramSplit[1];
        const paramName = paramSplit[paramSplit.length - 1].substring(
          0,
          paramSplit[paramSplit.length - 1].length - 1,
        );

        if (
          statusMap.get(parentTask) &&
          statusMap.get(parentTask)!['status']['conditions'][0]['type'] === 'Succeeded'
        ) {
          const parentId = statusMap.get(parentTask)!['status']['podName'];
          edges.push({ parent: parentId, child: ownerTask === '' ? componentId : ownerTask });

          // Add the taskResults value to the params value in status
          for (const result of statusMap.get(parentTask)!['status']['taskResults'] || []) {
            if (result['name'] === paramName) paramValue = result['value'];
          }
        }
      }
      // Find the output that matches this input and pull the value
      if (
        statusMap.get(component['name']) &&
        statusMap.get(component['name'])['status']['taskSpec']
      ) {
        for (const statusParam of statusMap.get(component['name'])!['status']['taskSpec']['params'])
          if (statusParam['name'] === param['name']) statusParam['value'] = paramValue;
      }
    }

    return edges;
  }

  public static getStatus(execStatus: any): NodePhase {
    return execStatus!.status.conditions[0].reason;
  }
}
