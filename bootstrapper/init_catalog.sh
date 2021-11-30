#!/bin/sh

# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0

# If no options are given, use environment variable
MLX_API_SERVER=${MLX_API_SERVER:-'localhost:80'}

# Print full usage details
print_usage () {
  # Max output line length is 80, arbitrarily.
  echo 'Usage: init_catalog.sh [OPTION...]'
  echo '  --host=HOST    Use the specified server host. Must be given alongside --port.'
  echo '  --port=PORT    Use the specified server port. Must be given alongside --host.'
  echo '  --disable-run  Disable Inference Services & Kubeflow Pipeline execution.'
  echo '                 Necessary when using Docker Compose instead of Kubernetes.'
  echo '  --help         Display this help text & exit.'
  echo
  echo 'If either the host or the port is not specified, the entire address defaults to'
  echo "MLX_API_SERVER ($MLX_API_SERVER)"
  exit 0
}

# Handle user input for server & port
HOST=''
PORT=''
DISABLE_RUN=''
while [ -n "$1" ]; do
  case $1 in
  --host=*) HOST="${1#???????}" ;; # "${var:start}" syntax is not a POSIX feature
  --port=*) PORT="${1#???????}" ;;
  --disable-run) DISABLE_RUN=1 ;;
  --help) print_usage ;;
  *)
    echo "init_catalog.sh: Option \"$1\" not recognized" >&2
    echo "For more info, try \"init_catalog.sh --help\"" >&2
    exit 1 ;;
  esac
  shift
done

# Build URL from arguments if all are specified
if [ -n "$HOST" ] && [ -n "$PORT" ]; then
  MLX_API_ADDRESS=$HOST:$PORT
  echo "API address: $MLX_API_ADDRESS"
else
  MLX_API_ADDRESS=$MLX_API_SERVER
  echo "API server or port not specified; using MLX_API_SERVER ($MLX_API_SERVER)"
fi

MLX_API_URL="http://$MLX_API_ADDRESS/apis/v1alpha1"


# Main functionality

# Wait for the MLX API server, but more importantly the MySQL server, to be ready
until curl -X GET -H 'Accept: application/json' -s "$MLX_API_URL/health_check?check_database=true&check_object_store=true" | grep -q 'Healthy'; do
  echo 'Waiting for MLX-API, Minio, MySQL ...'
  sleep 1
done

# Echo the MLX API server status (should be "Healthy")
curl -X GET -H 'Accept: application/json' -s "$MLX_API_URL/health_check?check_database=true&check_object_store=true"

# Upload the pipeline asset catalog
curl -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' -d @catalog_upload.json -s "$MLX_API_URL/catalog" | grep -iE "total_|error"

# [Obsolete] Mark all the catalog assets as approved and featured
# for asset_type in components datasets models notebooks pipelines; do
#   curl -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' -d '["*"]' -s "$MLX_API_URL/$asset_type/publish_approved"
#   curl -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' -d '["*"]' -s "$MLX_API_URL/$asset_type/featured"
# done

if [ -n "$DISABLE_RUN" ]; then
  # Disable the Inference Services, since we don't have a KFP cluster
  curl -X PUT -H 'Content-Type: application/json' -H 'Accept: application/json' -d '{"Inference Services": false}' -s "$MLX_API_URL/settings" -o /dev/null --show-error

  # Disable pipeline execution, since we don't have a KFP cluster
  curl -X PUT -H 'Content-Type: application/json' -H 'Accept: application/json' -d '{"Execution enabled": false}' -s "$MLX_API_URL/settings" -o /dev/null --show-error
fi
