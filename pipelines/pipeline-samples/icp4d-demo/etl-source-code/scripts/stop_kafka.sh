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
# stop_kafka.sh
#
# Script to shut down the cluster that start_kafka.sh starts.
#
# Run this script from the root of the project directory.
#

# Note that these need to be kept in sync with install_kafka.sh
KAFKA_VERSION="2.3.0"
SCALA_VERSION="2.12"

ENV_DIR="${PWD}/env"
KAFKA_ROOT="${ENV_DIR}/kafka_${SCALA_VERSION}-${KAFKA_VERSION}"

if [ ! -d "${KAFKA_ROOT}" ]
then
    echo "Kafka directory ${KAFKA_ROOT}"
    echo "Not found. Please run scripts/install_kafka.sh"
    exit
fi

pushd $KAFKA_ROOT

# Use the scripts provided by the Kafka distro for now.
# These scripts likely
./bin/zookeeper-server-stop.sh
./bin/kafka-server-stop.sh

popd

