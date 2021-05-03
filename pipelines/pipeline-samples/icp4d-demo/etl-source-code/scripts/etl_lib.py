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
# etl_lib.py
#
# Common routines shared between the notebook and Python script variants of
# the ETL job for the refrigerated containers demo.
#
# NOTE: You must start up PySpark BEFORE importing this file.

# Python library imports
import io
from typing import *

# 3rd-party library imports
import confluent_kafka as kafka
import numpy as np
import pandas as pd
import psycopg2

# The convention with PySpark is to do imports Java-style, one class per line.
from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import pandas_udf, PandasUDFType


def _make_consumer(kafka_bootstrap_servers: str) -> kafka.Consumer:
    """Shared code for creating Kafka consumers with sensible
    default parameters.

    Args:
        kafka_bootstrap_servers: Connection string for Kafka

    """
    return kafka.Consumer({
        "group.id": "my-etl-group",
        "bootstrap.servers": kafka_bootstrap_servers,
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False
    })


def get_partition_ids(kafka_bootstrap_servers: str,
                       kafka_topic: str) -> List[str]:
    """
    Retrieve a partition info for the target topic.

    Uses parameters in the global PARAMS variable:
        PARAMS["KAFKA_BOOTSTRAP_SERVERS"]
        PARAMS["KAFKA_TOPIC"]
    """
    c = _make_consumer(kafka_bootstrap_servers)
    # "list_topics" === "retrieve exhaustive metadata about cluster".
    # Drill down through the resulting nested structure.
    cluster_meta = c.list_topics()
    topic_info = cluster_meta.topics[kafka_topic]
    partition_ids = list(topic_info.partitions.keys())
    c.close()
    return partition_ids

#@pandas_udf("partition_id long, offset long, value string",
#            PandasUDFType.GROUPED_MAP)
def fetch_udf(params):
    """
    PySpark UDF to fetch available messages from the Kafka cluster,
    starting at the most recent commit point according to Kafka's own
    internal log.

    Joins a Kafka group and lets Kafka handle partition assignments.

    Does NOT commit offsets to Kafka.

    NOTE: Because PySpark doesn't deal well with the concept of modules,
    your Spark application will need to wrap this function itself.
    The process to follow is:
    1. Start up a SparkSession
    2. `spark.sparkContext.addPyFile(etl_lib.__file__)`
    3. ```
        fetch_udf = pandas_udf(etl_lib.fetch_udf,
                               "partition_id long, offset long, value string",
                               PandasUDFType.GROUPED_MAP)
       ```

    Arguments:
        params: One-line dataframe containing information on how to connect
                to Kafka. Columns of this dataframe:
            partition_id: Which Kafka partition to fetch from
            bootstrap_servers: String to pass for the eponymous argument
                when connecting to Kafka
            topic_name: Name of Kafka topic to subscribe to

    Returns a Pandas dataframe with the schema (partition_id, offset, message)
    """
    partition_ix = params["partition_id"][0]
    bootstrap_servers = params["bootstrap_servers"][0]
    topic_name = params["topic_name"][0]

    max_messages = 100000

    # NOTE: Timeouts MUST be several seconds, or Kafka won't reliably return
    # any data, even when running locally.
    timeout_sec = 10.0

    c = _make_consumer(bootstrap_servers)

    c.assign([kafka.TopicPartition(topic_name, partition_ix)])
    msgs = c.consume(num_messages=max_messages, timeout=timeout_sec)
    c.close()

    # Convert list of surrogate objects to a list of tuples and then to a dataframe.
    msg_tuples = [
        (partition_ix, m.offset(), m.value()) for m in msgs
    ]

    # Convert buffered data to a dataframe.
    return pd.DataFrame.from_records(msg_tuples,
                                     columns=["partition_id", "offset", "value"])


#@pandas_udf("partition_id long, offset long",
#            PandasUDFType.GROUPED_MAP)
def load_udf(records, params: Dict[str,Any]):
    """
    PySpark UDF that bulk-loads records into the database.

    Assumes that the column names in the incoming JSON records are the same as
    the column names in the target table.

    NOTE: Because PySpark doesn't deal well with the concept of modules,
    your Spark application will need to wrap this function with an additional
    layer of Python code. The process to follow is:
    1. Start up a SparkSession
    2. Create a broadcast variable PARAMS in your SparkSession containing
       a python dictionary with Postgres parameters under the following keys:
       ("postgres_host", "postgres_port", "postgres_db", "postgres_user",
        "table_name")
       To use the default value for any of these parameters, set the associated
       dictionary entry to None.
       For example:
          params_broadcast = spark.sparkContext.broadcast(my_dict)
    3. `spark.sparkContext.addPyFile(etl_lib.__file__)`
    4. Define a wrapper UDF function inside a Python context that has access to
       your broadcast variable:
       ```
       @pandas_udf("partition_id long, offset long", PandasUDFType.GROUPED_MAP)
       def load_udf(records):
           return etl_lib.load_udf(records, params_broadcast.value)
       ```
       This step is necessary because PySpark UDFs can only pick up broadcast
       variables that `pickle` can see when serializing a function.

    Arguments:
        records: Pandas dataframe in the format returned by fetch_udf
        params: Dictionary containing Postgres connection parameters

    Returns a Pandas dataframe with the schema (partition_id, offset)
    containing the metadata for all records successfully loaded.
    """
    # The LOAD command needs column names and CSV data.
    # Convert JSON =>  Dataframe => (CSV and column names)
    json_buf = io.StringIO("\n".join(records["value"]))
    df = pd.read_json(json_buf, orient="records", lines=True)
    col_names = tuple(df.columns)

    def _make_conn():
        return psycopg2.connect(
            host=params["postgres_host"],
            port=params["postgres_port"],
            database=params["postgres_db"],
            user=params["postgres_user"],
            password=params["postgres_password"]
        )

    try:
        # Fast path: Bulk insert of all records, no errors.
        # Note that the cursor will automatically roll back the current
        # transaction if an exception is thrown; and will automatically
        # commit when exiting the with block if no exceptions happen.
        with _make_conn() as conn:
            with conn.cursor() as cur:
                csv_str = df.to_csv(index=False, header=False)
                csv_buf = io.StringIO(csv_str)
                cur.copy_from(csv_buf, params["table_name"],
                              columns=col_names, sep=",")
    except psycopg2.IntegrityError as fast_path_error:
        print("**** Fast path raised error: {}".format(fast_path_error))
        print("**** Retrying insertion one record at a time")
        # Slow path: Insert 1 at a time, log errors
        for i in range(len(df.index)):
            # Separate connection for every record.
            with _make_conn() as conn:
                with conn.cursor() as cur:
                    # Note single-value list as arg to iloc so we get back a
                    # pd.DataFrame instead of pd.Series
                    csv_str = df.iloc[[i]].to_csv(index=False, header=False)
                    csv_buf = io.StringIO(csv_str)
                    cur = conn.cursor()
                    try:
                        cur.copy_from(csv_buf, params["table_name"],
                                      columns=col_names, sep=",")
                    except psycopg2.IntegrityError as slow_path_error:
                        print("Logging error at offset {}: {}"
                              "".format(records["offset"].iloc[i],
                                        slow_path_error))

    # If we get here, either the fast path or the slow path completed
    return records[["partition_id", "offset"]]


def commit_offsets(partition_offset_pairs: List[Tuple[int, int]],
                   kafka_bootstrap_servers: str,
                   kafka_topic: str):
    """
    Tell Kafka that we have consumed all messages up to a set of offsets.

    Args:
        partition_offset_pairs: List of commit offsets by partition.
            Must have exactly one offset per partition.
        kafka_bootstrap_servers: Kafka connection string
    """
    c = _make_consumer(kafka_bootstrap_servers)
    c.commit(offsets=[
        kafka.TopicPartition(kafka_topic, partition, offset)
        for partition, offset in partition_offset_pairs
    ])
    c.close()

