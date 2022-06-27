# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0
from __future__ import print_function

import json
import kfp

from kfp_server_api import ApiListExperimentsResponse
from kfp_server_api import ApiListRunsResponse, ApiResourceType, ApiRunDetail
from kfp_server_api.rest import ApiException
from os import environ as env  # noqa: F401
from pprint import pprint  # noqa: F401


# export AMBASSADOR_SERVICE_HOST=$(kubectl get nodes -o jsonpath='{.items[0]..addresses[?(@.type=="ExternalIP")].address}')
# export AMBASSADOR_SERVICE_PORT=$(kubectl -n kubeflow get service ambassador -o jsonpath='{.spec.ports[0].nodePort}')
kfp_host = env.get("AMBASSADOR_SERVICE_HOST")
kfp_port = env.get("AMBASSADOR_SERVICE_PORT")

url = f"{kfp_host}:{kfp_port}/pipeline"


def get_kfp_client() -> kfp.Client:
    kfp_client = kfp.Client(url)
    return kfp_client


def print_function_name_decorator(func):
    def wrapper(*args, **kwargs):
        print()
        print(f"---[ {func.__name__}{args}{kwargs} ]---")
        print()
        return func(*args, **kwargs)

    return wrapper


@print_function_name_decorator
def list_runs(experiment_name: str = None):

    kfp_client = get_kfp_client()

    experiments = []

    if experiment_name:

        # https://github.com/kubeflow/pipelines/blob/3e7a89e044d0ce448ce0b7b2c894a483487694a1/backend/api/filter.proto#L24-L63
        experiment_filter_dict = {
            "predicates": [
                {
                    "key": "name",
                    "op": "IS_SUBSTRING",  # "EQUALS",
                    "string_value": experiment_name,
                }
            ]
        }

        experiment_response: ApiListExperimentsResponse = (
            kfp_client._experiment_api.list_experiment(
                page_size=100,
                sort_by="created_at desc",
                filter=json.dumps(experiment_filter_dict),
            )
        )

        if experiment_response.experiments:
            experiments = [
                e for e in experiment_response.experiments if experiment_name in e.name
            ]
        else:
            print(f"Experiment(s) with name '{experiment_name}' do(es) not exist.")

    runs = []

    if experiments:
        for experiment in experiments:
            run_response: ApiListRunsResponse = kfp_client._run_api.list_runs(
                page_size=100,
                sort_by="created_at desc",
                resource_reference_key_type=ApiResourceType.EXPERIMENT,
                resource_reference_key_id=experiment.id,
            )

            runs.extend(run_response.runs or [])

    else:
        run_response: ApiListRunsResponse = kfp_client._run_api.list_runs(
            page_size=100, sort_by="created_at desc"
        )

        runs.extend(run_response.runs or [])

    runs = sorted(runs, key=lambda r: r.created_at, reverse=True)
    for i, r in enumerate(runs):
        # pprint(r)
        print(
            "%2i: %s  %s  %s  (%s)"
            % (
                i + 1,
                r.id,
                r.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                r.name,
                r.status,
            )
        )

    return runs


@print_function_name_decorator
def stop_run(run_id):

    kfp_client = get_kfp_client()

    try:
        run_stop_response = kfp_client._run_api.terminate_run(run_id=run_id)
        pprint(run_stop_response)

    except ApiException as e:

        if e.status == 404:

            run_detail: ApiRunDetail = kfp_client._run_api.get_run(run_id=run_id)

            if run_detail:  # and run_detail.run.status in ["Failed", "Error"]:
                workflow_manifest = json.loads(
                    run_detail.pipeline_runtime.workflow_manifest
                )
                # pods = filter(lambda d: d["type"] == 'Pod', list(workflow_manifest["status"]["nodes"].values()))
                pods = [
                    node
                    for node in list(workflow_manifest["status"]["nodes"].values())
                    if node["type"] == "Pod"
                ]
                if pods:
                    print(f"{e.status}, {e.reason}: {pods[0]['message']}")
                else:
                    print(
                        f"Run with id '{run_id}' could not be terminated. No pods in 'Running' state?"
                    )
        else:
            print(e)


@print_function_name_decorator
def delete_run(run_id):

    kfp_client: kfp.Client = get_kfp_client()

    try:
        run_delete_response = kfp_client._run_api.delete_run(id=run_id)
        pprint(run_delete_response)

    except AttributeError as e:
        # ignore KFP AttributeError. It is a bug in the Swagger-generated client code for Kubeflow Pipelines
        if not str(e) == "module 'kfp_run.models' has no attribute 'ERRORUNKNOWN'":
            raise e

    except ApiException as e:

        if e.status == 404:

            run_detail: ApiRunDetail = kfp_client._run_api.get_run(run_id=run_id)

            if run_detail:  # and run_detail.run.status in ["Failed", "Error"]:
                workflow_manifest = json.loads(
                    run_detail.pipeline_runtime.workflow_manifest
                )
                # pods = filter(lambda d: d["type"] == 'Pod', list(workflow_manifest["status"]["nodes"].values()))
                pods = [
                    node
                    for node in list(workflow_manifest["status"]["nodes"].values())
                    if node["type"] == "Pod"
                ]
                if pods:
                    print(pods[0]["message"])
                else:
                    print(
                        f"Run with id '{run_id}' could not be deleted. No corresponding pods."
                    )
        else:
            print(e)


if __name__ == "__main__":

    # runs = list_runs()
    # runs = list_runs(experiment_name="COMPONENT_RUNS")
    # runs = list_runs(experiment_name="MODEL_RUNS")
    runs = list_runs(experiment_name="_RUN")

    for r in runs[-5:]:
        # stop_run(r.id)
        delete_run(r.id)
