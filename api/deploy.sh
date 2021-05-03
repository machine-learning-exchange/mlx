#!/usr/bin/env bash

# Copyright 2021 IBM Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
#
#     http://www.apache.org/licenses/LICENSE-2.0 
#
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License. 


SCRIPT_DIR="$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )"

cd "$SCRIPT_DIR"


# TODO: parameter processing, ... --nodePort=32123
NODE_PORT=32123


echo "Checking for working Kubernetes cluster with Kubeflow Pipelines ..."

if ! kubectl get pods --all-namespaces | grep -q ml-pipeline; then
    echo "We need a cluster with Kubeflow Pipelines deployed!"
    exit 1
fi

if [ -z "$POD_NAMESPACE" ]; then
    POD_NAMESPACE=$(kubectl get svc --all-namespaces | grep ml-pipeline | head -1 | cut -d " " -f1)
fi

if [ -z "$PUBLIC_IP" ]; then
    PUBLIC_IP=$(kubectl get nodes -o jsonpath='{.items[].status.addresses[?(@.type=="ExternalIP")].address}')
fi

SETTINGS_FILE="settings_${PUBLIC_IP}.json"

# replace the namespace in the deployment spec, we need it in there to define the POD_NAMESPACE env var
#sed -i.before "s/namespace: .*/namespace: ${POD_NAMESPACE}/g" server/mlx-api.yml
#mv -f server/mlx-api.yml.before server/mlx-api.yml
sed "s/namespace: .*/namespace: ${POD_NAMESPACE}/g" server/mlx-api.yml > deploy-api-server.yml


# check for existing deployment
if kubectl -n "${POD_NAMESPACE}" get pods | grep -q mlx-api; then

    NODE_PORT=$(kubectl -n "${POD_NAMESPACE}" get service mlx-api -o jsonpath='{.spec.ports[0].nodePort}')

    echo "The existing MLX API server is listening on nodePort=${NODE_PORT}"

    # get the API service IP, the existing API service may not have gotten deployed on the same node as the PUBLIC_IP
    for ip in $(kubectl get nodes -o jsonpath='{.items[*]..addresses[?(@.type=="ExternalIP")].address}'); do
        curl -X OPTIONS -m 1 -s "http://${ip}:${NODE_PORT}/apis/v1alpha1/health_check" \
            && export PUBLIC_IP=${ip} \
            && break
    done

    EXISTING_VERSION=$(kubectl -n "${POD_NAMESPACE}" get pods --selector=service=mlx-api -o jsonpath='{.items[*].metadata.labels.version}' | head -1)
    echo "Existing version: '${EXISTING_VERSION}'"

    NEW_VERSION=$(grep version deploy-api-server.yml | grep -vE "^#" | awk '{print $2}')
    echo "New version: '${NEW_VERSION}'"

    if [[ "${NEW_VERSION}" == "${EXISTING_VERSION}" ]]; then
        echo "Same version was already deployed!"
        read -r -t 10 -n1 -p "Continue redeployment (y/n)? " key || key=n
        case ${key} in
            y|Y|"" )  echo Yes  ;;  # hitting ENTER without typing "y" will suffice
            * )       echo No   ; exit 1 ;;
        esac
    fi

    if [ -z "$PUBLIC_IP" ]; then
        echo "PUBLIC_IP is required to backup application settings"
        exit 1
    else
        echo "Save current application settings in file '${SETTINGS_FILE}'"
        curl -X GET "http://${PUBLIC_IP}:${NODE_PORT}/apis/v1alpha1/settings" -o "${SETTINGS_FILE}" -s
    fi

    echo "Deleting existing deployment..."

    kubectl -n "${POD_NAMESPACE}" -f deploy-api-server.yml delete

    if grep -q -E "^[ ]+nodePort: 3" server/mlx-api.yml; then

        echo -n "Waiting for pod to be terminated"

        while kubectl -n "${POD_NAMESPACE}" get pods | grep -q mlx-api; do
            sleep 1
            echo -n "."
        done

        # add some extra sleep time to make sure nodePort has been made available again
        for i in $(seq 5); do
            sleep 1
            echo -n "."
        done

        echo "done"
    fi
fi


echo "Deploying MLX API server..."

kubectl -f deploy-api-server.yml apply

# if we failed to deploy, delete and exit
if ! kubectl -n "${POD_NAMESPACE}" get svc | grep -q "mlx-api"; then

    kubectl -n "${POD_NAMESPACE}" -f deploy-api-server.yml delete
    exit 1
fi


echo "Waiting for pod to be ready..."

end=$((SECONDS+30))

while ! kubectl -n "${POD_NAMESPACE}" get pods | grep -q -E "mlx-api-.* Running " ; do

    sleep 1
    echo -n "."

    if (( SECONDS > end )); then
        echo "timed out"
        kubectl -n "${POD_NAMESPACE}" get pods | grep "mlx-api-"
        exit 1
    fi
done
echo "done"


if [[ -n "${NODE_PORT}" ]]; then

    echo "Setting nodePort to ${NODE_PORT} ..."

    for i in $(seq 1 5); do

        kubectl -n "${POD_NAMESPACE}" patch svc mlx-api --type='json' \
            -p "[{ \"op\": \"replace\", \"path\": \"/spec/ports/0/nodePort\", \"value\": $NODE_PORT }]" \
            && exit_code=0 && break || exit_code=$? && sleep 10
    done

    if (( exit_code > 0 )); then
        echo "Error"
        exit ${exit_code}
    fi
fi


if kubectl -n "${POD_NAMESPACE}" get pods | grep -q mlx-api; then

    if [ -z "$PUBLIC_IP" ]; then

        echo "PUBLIC_IP is required to initialize application settings"
    else

        API_PORT=$(kubectl get service mlx-api -n ${POD_NAMESPACE} -o jsonpath='{.spec.ports[0].nodePort}')
#        API_PORT=$NODE_PORT
        KFP_PORT=$(kubectl get service ml-pipeline-ui -n ${POD_NAMESPACE} -o jsonpath='{.spec.ports[0].nodePort}')

        # wait for API to be ready
        end=$((SECONDS+30))

        echo -n "Waiting for API server (http://${PUBLIC_IP}:${API_PORT}/apis/v1alpha1/settings)"

        until $(curl -o /dev/null -s --head -I "http://${PUBLIC_IP}:${API_PORT}/apis/v1alpha1/settings"); do
            echo -n "."
            sleep 1
            if (( SECONDS > end )); then
                echo "Curl timed out"
                exit 1
            fi
        done

        echo

        if [ -s "${SETTINGS_FILE}" ] ; then

            echo "Re-instating the settings from the previous deployment"

            curl -X POST "http://${PUBLIC_IP}:${API_PORT}/apis/v1alpha1/settings" -s \
                -H "Content-Type: application/json" \
                -d @${SETTINGS_FILE} | \
            grep -q "sections" && echo "success" || echo "failed to re-instate previous application settings"

        else
            echo "Could not re-instate application settings due to missing or empty file '$SETTINGS_FILE'"
        fi

        echo -n "Initializing application settings with host and port..."

        curl -X PUT "http://${PUBLIC_IP}:${API_PORT}/apis/v1alpha1/settings" -s \
            -H "Content-Type: application/json" \
            -d "{\"API Endpoint\": \"${PUBLIC_IP}:${API_PORT}\", \
                 \"KFP API\": \"${PUBLIC_IP}:${KFP_PORT}\"}" | \
            grep -q "${PUBLIC_IP}:${API_PORT}" && echo "success" || ( echo "failed" && exit 1 )
    fi
fi


# show deployment results
echo
kubectl -n "${POD_NAMESPACE}" get svc | grep -E "NAME|mlx-api" | column -t
echo
kubectl -n "${POD_NAMESPACE}" get pod | grep -E "NAME|mlx-api" | column -t


# delete temporary deployment YAML file
rm -f deploy-api-server.yml

# delete backup settings JSON file
rm -f "${SETTINGS_FILE}"

# change back to original working directory
cd -  > /dev/null

command -v say > /dev/null && say "The M L X A P I server was deployed successfully"
