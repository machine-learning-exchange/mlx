# removes all containers and volumes and pulls the latest source and contaimer images

# remove all containers
for c in `docker container ls -a |grep quickstart |awk '{print $1}'`; do docker rm $c; done

# remove all volumes
docker volume rm quickstart_data-minio
docker volume rm quickstart_data-mysql

# get latest source code
git pull

# get latest container images
docker-compose pull
