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
#! /usr/bin/env python3

################################################################################
# push.py
#
# Push some example records to the Kafka topic.
#
# To run from the root of the project:
#   PYTHONPATH=$PWD python scripts/push.py
#
# Run with "--help" option for a list of available arguments.

import argparse
import os
import sys

import confluent_kafka as kafka
import pandas as pd

import json
import io

# Note that this import requires that the project root be on $PYTHONPATH
import reefer.simulator.domain.reefer_simulator as sim


########################################
# ARGUMENTS

parser = argparse.ArgumentParser(description="ETL from Kafka to Spark to Postgres")
parser.add_argument("--kafka_bootstrap_servers", type=str, default="localhost:9092",
                    help="Connection string for Kafka (default: localhost:9092)")
parser.add_argument("--kafka_topic", type=str, default="reefer",
                    help="Name of Kafka topic to monitor (default: reefer)")
parser.add_argument("--container_id", type=str, default="C0001",
                    help="Container ID string"
                         "(default: 'C0001')")
parser.add_argument("--num_records", type=int, default=10,
                    help="Number of records to send"
                         "(default: 10)")
parser.add_argument("--record_type", type=str, default="normal",
                    help="Type of records to send: can be 'normal', 'co2', or 'power'"
                         "(default: 'normal')")

########################################
# MAIN

def main():
    args = parser.parse_args()
    args_as_dict = { k: getattr(args, k) for k in args.__dict__.keys() }

    print("Generating records.")
    data_gen = sim.ReeferSimulator()
    if args.record_type == "normal":
        df = data_gen.generateNormalRecords(cid=args.container_id,
                                            nb_records=args.num_records)
    elif args.record_type == "co2":
        df = data_gen.generateCo2Records(cid=args.container_id,
                                            nb_records=args.num_records)
    elif args.record_type == "power":
        df = data_gen.generatePowerOffRecords(cid=args.container_id,
                                              nb_records=args.num_records)
    else:
        raise ValueError("Unknown record type '{}'".format(args.record_type))
    print("Generated records:\n{}".format(df))

    # Convert to lines of JSON data
    json_str = df.to_json(orient="records", lines=True)
    json_lines = json_str.split("\n")
    print("First 3 records as JSON:\n{}".format(json_lines[:3]))

    # Verify that the JSON is valid by trying to parse it into a dataframe
    print("Validating JSON.")
    json_buf = io.StringIO("\n".join(json_lines))
    print("JSON unpacks to:\n{}".format(
            pd.read_json(json_buf, orient="records", lines=True)))

    # Send each line of JSON data as a separate Kafka message.
    print("Sending data to Kafka cluster at {} on topic "
          "{}".format(args.kafka_bootstrap_servers, args.kafka_topic))
    prod = kafka.Producer({
        "bootstrap.servers" : args.kafka_bootstrap_servers
    })
    for l in json_lines:
        prod.produce(topic=args.kafka_topic, value=l.encode("utf-8"))
    print("Flushing outgoing Kafka data streams")
    prod.flush()


if __name__ == "__main__":
    main()



