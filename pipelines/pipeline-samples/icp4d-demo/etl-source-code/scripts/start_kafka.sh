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
# start_kafka.sh
#
# Script to start a localhost-only single-node Kafka cluster.
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

# Run zookeeper with the config created by install_kafka.sh
# Rather than go through the trouble of configuring log4j, we just run in
# console mode and redirect to STDOUT and STDERR to a file.
./bin/zookeeper-server-start.sh zk.cfg 2>&1 > zk.log &

# Can't start Kafka until zookeeper is started.
# Rather than write a programmatic test for zookeeper, just wait 10 seconds.
echo "Waiting for zookeeper to start..."
sleep 10

# Run kafka with the config created by install_kafka.sh
./bin/kafka-server-start.sh kafka.cfg 2>&1 > kafka.log &
popd

# Wait a moment before we echo log output to stdout
sleep 5

echo "Kafka and Zookeeper should be started."
echo "Last 3 lines of Zookeeper log:"
tail -3 ${KAFKA_ROOT}/zk.log
echo "---------------------------------------------------------------------"
echo "Last 3 lines of Kafka log:"
tail -3 ${KAFKA_ROOT}/kafka.log
echo "---------------------------------------------------------------------"
echo "Kafka should be listening on localhost on port 9092."
echo "Log output should be at:"
echo "(zookeeper) ${KAFKA_ROOT}/zk.log"
echo "    (kafka) ${KAFKA_ROOT}/kafka.log"
echo "To shut everything down, run ./scripts/stop_kafka.sh"

