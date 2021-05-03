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
#! /bin/bash

################################################################################
# install_kafka.sh
#
# Script to perform the surprisingly complex task of setting up a dead-simple
# localhost-only single-node Kafka cluster.
#
# To install on the local machine, run this script from the root of the project
# directory with no arguments.
#
# To install inside a Docker container, set the environment variable
# KAFKA_BASE to the directory where you want to install Kafka. Also set the
# environment variable KAFKA_LISTEN_HOST to 0.0.0.0 if you want to advertise
# on the container's external network interfaces.
#
# To start and stop the installed Kafak on a workstation, use the scripts
# start_kafka.sh and stop_kafka.sh.
#
# On a Docker container, use start_kafka_docker.sh to start and kill the
# container to stop.
#

KAFKA_VERSION="2.3.0"
SCALA_VERSION="2.12"

if [ -z ${KAFKA_BASE} ]
then
    # Local development install. This script installs everything under ./env.
    # Make sure env exists first.
    ENV_DIR="${PWD}/env"
    if [ ! -d "${ENV_DIR}" ]
    then
        echo "Anaconda environment not found at ${ENV_DIR}."
        echo "Please run this script from the root of the project after running "
        echo "scripts/env.sh"
        exit
    fi
    KAFKA_BASE="${ENV_DIR}"
fi

if [ ! -d "${KAFKA_BASE}" ]
then
    echo "Target directory ${KAFKA_BASE} not found. Exiting."
    exit
fi

# Note that we deliberately allow KAFKA_LISTEN_HOST to be set to an emtpy
# string
if [ -x ${KAFKA_LISTEN_HOST+x} ]
then
    KAFKA_LISTEN_HOST="localhost"
fi

echo "Installing into ${KAFKA_BASE}"

# Kafka insists on putting their binary packages behind a CGI script that
# generates a list of mirrors that a human is supposed to choose from.
# This is somewhat less than convenient for automation, so here we hard-code
# one of the mirrors.
# Generate an appropriate URL for wget.
DOWNLOAD_BASE="http://www.gtlib.gatech.edu/pub/apache/kafka"
TARBALL_NAME="kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz"
DIR_NAME="kafka_${SCALA_VERSION}-${KAFKA_VERSION}"
KAFKA_HOME="${KAFKA_BASE}/${DIR_NAME}"
DOWNLOAD_URL="${DOWNLOAD_BASE}/${KAFKA_VERSION}/${TARBALL_NAME}"

pushd $KAFKA_BASE
if [ ! -f "${TARBALL_NAME}" ]
then
    wget $DOWNLOAD_URL -O $TARBALL_NAME
fi
rm -rf $DIR_NAME
tar xvzf $TARBALL_NAME
cd $DIR_NAME

# Zookeeper needs a database directory. Create one here so it doesn't scribble
# all over /tmp
mkdir zk_data

# Generate a zookeeper config that references the data dir
cat > zk.cfg <<EOM
dataDir=${KAFKA_HOME}/zk_data
clientPort=2181
maxClientCnxns=0
EOM

# Kafka also needs a data directory. Create one here.
mkdir kafka_data

# Generate a Kafka config
cat > kafka.cfg <<EOM
# Minimal kafka.cfg for testing.

# Zookeeper port must be kept in sync with zk.cfg!
zookeeper.connect=localhost:2181

# No replication. Otherwise Kafka will get very upset with one broker.
offsets.topic.replication.factor=1
transaction.state.log.replication.factor=1
transaction.state.log.min.isr=1

# Host as configured by KAFKA_LISTEN_HOST, port 9092
listeners=PLAINTEXT://${KAFKA_LISTEN_HOST}:9092
EOM


popd

