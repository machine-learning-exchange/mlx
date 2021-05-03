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
################################################################################
# etl.py
#
# Spark-based ETL from Kafka to PostgreSQL.
#
# Accepts arguments on the command line to specify how to talk to Spark, Kafka,
# and Postgres.
#
# Run `python etl.py --help` for a list of available arguments.

########################################
# IMPORTS
import argparse
import functools
import io
import operator
import os
import time
import sys

import numpy as np
import pandas as pd
import psycopg2

import etl_lib

# The convention with PySpark is to import individual classes, Java-style
from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import pandas_udf, PandasUDFType
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
import pyspark
import confluent_kafka as kafka


########################################
# CONSTANTS


# Number of batches to divide our data into when loading into PostgreSQL.
# Since there's only one server, making this too high is not a good idea.
_NUM_BATCHES = 4

########################################
# ARGUMENTS

parser = argparse.ArgumentParser(description="ETL from Kafka to Spark to Postgres")
parser.add_argument("--spark_master", type=str, default="local[*]",
                    help="Connection string for Spark (default: local[*])")
parser.add_argument("--kafka_bootstrap_servers", type=str, default="localhost:9092",
                    help="Connection string for Kafka (default: localhost:9092)")
parser.add_argument("--kafka_topic", type=str, default="reefer",
                    help="Name of Kafka topic to monitor (default: reefer)")
parser.add_argument("--batch_temp_loc", type=str, default="batch.csv",
                    help="URL/path at which to write the current batch of records "
                         "(default: batch.csv)")
parser.add_argument("--postgres_host", type=str, default=None,
                    help="Address of PostgreSQL server (default: None)")
parser.add_argument("--postgres_port", type=int, default=None,
                    help="Port that Postgres server is listening on (default: None)")
parser.add_argument("--postgres_db", type=str, default="demo",
                    help="Name of PostgreSQL database to load (default: demo)")
parser.add_argument("--postgres_user", type=str, default=None,
                    help="User name to use when connecting to Postgres server "
                         "(default: None)")
parser.add_argument("--postgres_password", type=str, default=None,
                    help="Password to use when connecting to Postgres server "
                         "(default: None)")
parser.add_argument("--table_name", type=str, default="reefer_telemetries",
                    help="Name of target database table for load operation"
                         "(default: reefer_telemetries)")

# Append Postgres Credentials to argument dictionary
def append_postgres_creds(args_as_dict):
    postgresURL=urlparse(os.getenv('POSTGRES_URL').replace("'",""))
    args_as_dict['postgres_host'] = postgresURL.hostname
    args_as_dict['postgres_port'] = int(postgresURL.port)
    args_as_dict['postgres_db'] = postgresURL.path.replace('/', '')
    args_as_dict['postgres_user'] = postgresURL.username
    args_as_dict['postgres_password'] = postgresURL.password
    return args_as_dict

########################################
# SUBROUTINES

from subprocess import check_output
ip = check_output(['hostname', '-i']).decode().rstrip()

########################################
# MAIN

def main():
    args = parser.parse_args()
    args_as_dict = { k: getattr(args, k) for k in args.__dict__.keys() }

    args_as_dict = append_postgres_creds(args_as_dict)

    print("Connecting to Spark.")

    # Fire up PySpark.
    spark = SparkSession.builder \
        .master(args.spark_master) \
        .appName("ReeferETL") \
        .config("spark.driver.host", ip) \
        .config("spark.sql.execution.arrow.enabled", "true") \
        .getOrCreate()

    print("Connected to Spark. Connection object is: {}".format(spark))

    # Drop Postgres/Kafka connection parameters into a broadcast variable so
    # that our UDFs can pick them up.
    params_broadcast = spark.sparkContext.broadcast(args_as_dict)


    # Tell PySpark how to find the module with all our shared application
    # code.
    spark.sparkContext.addPyFile(etl_lib.__file__)

    # Define our UDFs. This must happen AFTER starting Spark.
    fetch_udf = pandas_udf(etl_lib.fetch_udf,
                       "partition_id long, offset long, value string",
                       PandasUDFType.GROUPED_MAP)
    @pandas_udf("partition_id long, offset long", PandasUDFType.GROUPED_MAP)
    def load_udf(records):
        return etl_lib.load_udf(records, params_broadcast.value)

    print("Connecting to Kafka cluster.");

    # Generate a dataframe for job control.
    partition_ids = etl_lib.get_partition_ids(args.kafka_bootstrap_servers,
                                            args.kafka_topic)
    params_df = spark.createDataFrame(
        [(p, args.kafka_bootstrap_servers, args.kafka_topic)
         for p in partition_ids],
        ["partition_id", "bootstrap_servers", "topic_name"])
    params_df.show()

    print("Fetching messages from Kafka.");
    # Fetch all available messages from all partitions in parallel and write
    # the resulting messages to a temp directory on the distributed filesystem.
    # Use CSV format for ease of debugging.
    raw_batch_df = (
        params_df
        # Work around Spark's tendancy to use spark.sql.shuffle.partitions blindly
        .repartition(len(partition_ids), "partition_id")
        .groupby("partition_id")
        .apply(fetch_udf)
    )
    #raw_batch_df.write.csv(path=args.batch_temp_loc, mode="overwrite",
    #                       header=True)
    # Wrap the temp file in a dataframe for all subsequent processing.
    #batch_df = spark.read.csv(args.batch_temp_loc, header=True,
    #                          schema=raw_batch_df.schema)
    raw_batch_df.toPandas().to_csv(args.batch_temp_loc, index=False)
    data = pd.read_csv(args.batch_temp_loc)
    batch_df = spark.createDataFrame(data, schema=raw_batch_df.schema)

    print("DataFrame for batch is {} with count = {}"
          "".format(batch_df, batch_df.count()))

    print("Loading records into database.");
    load_results = (
    batch_df
        # Work around Spark's tendancy to use spark.sql.shuffle.partitions blindly
        .withColumn("partition_id", batch_df.offset % _NUM_BATCHES)
        .repartition(_NUM_BATCHES, "partition_id")
        .groupby("partition_id")
        .apply(load_udf)
        .toPandas()
    )
    print("Records loaded by Kafka offset:\n{}".format(load_results))

    print("Committing offsets to Kafka.");
    offsets_df = batch_df.groupby("partition_id").agg({"offset": "max"})
    offsets_df = offsets_df.select(offsets_df["partition_id"],
                                   (offsets_df["max(offset)"] + 1).alias("to_commit"))
    offsets_pd = offsets_df.toPandas()
    print("Offsets to commit:\n{}".format(offsets_pd))

    etl_lib.commit_offsets(list(offsets_pd.to_records(index=False)),
                           args.kafka_bootstrap_servers,
                           args.kafka_topic)
    print("Done.")

if __name__ == "__main__":
    main()


