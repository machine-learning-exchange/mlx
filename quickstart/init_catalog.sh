#!/bin/sh

MLX_API_SERVER=${MLX_API_SERVER:-"localhost:8080"}
MLX_API_URL="http://${MLX_API_SERVER}/apis/v1alpha1"

# wait for the MLX API server, but more importantly the MySQL server to be ready
until curl -X GET -H 'Accept: application/json' -s "${MLX_API_URL}/health_check?check_database=true&check_object_store=true" | grep -q 'Healthy'; do
  echo 'Waiting for MLX-API, Minio, MySQL ...'
  sleep 1
done

# echo the MLX API server status, should be "Healthy"
curl -X GET -H 'Accept: application/json' -s "${MLX_API_URL}/health_check?check_database=true&check_object_store=true"

# upload the pipeline asset catalog
curl -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' -d @catalog_upload.json -s "${MLX_API_URL}/catalog" | grep -iE "total_|error"

# mark all the catalog assets as approved and featured
for asset_type in components datasets models notebooks pipelines; do
  curl -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' -d '["*"]' -s "${MLX_API_URL}/$asset_type/publish_approved"
  curl -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' -d '["*"]' -s "${MLX_API_URL}/$asset_type/featured"
done

# disable the Inference Services, since we don't have a KFP cluster
curl -X PUT -H 'Content-Type: application/json' -H 'Accept: application/json' -d '{"Inference Services": false}' -s "${MLX_API_URL}/settings" -o /dev/null --show-error

# disable pipeline execution, since we don't have a KFP cluster
curl -X PUT -H 'Content-Type: application/json' -H 'Accept: application/json' -d '{"Execution enabled": false}' -s "${MLX_API_URL}/settings" -o /dev/null --show-error
