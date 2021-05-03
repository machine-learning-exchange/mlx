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
# load_db.py
#
# Bulk-load the larger tables of the warehouse with generated historical data.
#
# Will use the following environment variables to find the database, if
# present:
#   LOAD_DB_POSTGRES_IP (IP address of server)
#   LOAD_DB_POSTGRES_PORT (TCP port for connecting to server)
#   LOAD_DB_POSTGRES_DB (Name of database)
#   LOAD_DB_POSTGRES_USER
#   LOAD_DB_POSTGRES_PASSWORD
#
# To run from the root directory of the project, run as follows:
#
# PYTHONPATH=$PWD python scripts/load_db.py

import datetime
import io
import os
import numpy as np
import pandas as pd
import psycopg2
import time

from typing import List, Sequence, Any


import reefer.simulator.domain.reefer_simulator as sim


################################################################################
# CONSTANTS

_DEFAULT_DB_NAME = "demo"

# How many containers should be represented in the CONTAINER table.
# populate_tables.sql only contains 10 containers.
# We add additional dummy rows to get up to this target number.
_NUM_CONTAINERS = 1000

# How many rows of dummy time series data to load for each container.
_ROWS_PER_CONTAINER = 1000

# Time (in hours) between rows of the generated time series.
# Note that changing this constant will NOT change the data generator.
_HOURS_PER_ROW = 0.25   # i.e. 15 minutes

# Dataframe column name ==> table column name for Container_Telemetry table
# DISABLED because (at least for now) the data generator's column names are
# sync'd with the table's column names.
#_DF_COLS_TO_TABLE_COLS = {
#    "Timestamp" : "measurement_time",
#    "ID" : "container_id",
#    "Temperature(celsius)": "temperature",
#    "Target_Temperature(celsius)": "target_temperature",
#    "Power": "kilowatts",
#    "PowerConsumption": "kilowatt_hours",
#    "ContentType": "content_type",
#    "O2": "oxygen_level",
#    "CO2": "carbon_dioxide_level",
#    "Time_Door_Open": "time_door_open",
#    "Defrost_Cycle": "defrost_cycle",
#}
#_DF_COLS = _DF_COLS_TO_TABLE_COLS.keys()
#_TABLE_COLS = _DF_COLS_TO_TABLE_COLS.values()


# ID strings for the REEFER_MODEL column of the REEFERS table
_REEFER_MODELS = [ "20RF", "40RH", "45RW" ]

# Commands to create the internal table(s) that this script adds to the
# standard schema.
_CREATE_DDL = """
-- Metadata used by the data generator, stored in the database for
-- reference and debugging purposes.
create table if not exists data_gen_meta(
    container_id varchar(64) UNIQUE NOT NULL,
    failure_type varchar(16), -- 'none', 'co2', or 'power'
    product_id varchar(64),
    foreign key (container_id) references reefers(container_id),
    foreign key (product_id) references products(product_id)
);

create table if not exists labels(
    container_id varchar(64) NOT NULL,
    measurement_time TIMESTAMP NOT NULL,
    maintenance_required INT,
    primary key (container_id, measurement_time),
    foreign key (container_id, measurement_time) references
        reefer_telemetries(container_id, measurement_time)
);

-- Views for quickly extracting training data for CO2 or power-off models
create or replace view CO2_Training_Data as
select T.* -- , L.maintenance_required
from reefer_telemetries T, labels L, data_gen_meta M
where
  T.container_id = M.container_id
  and L.container_id = T.container_id
  and T.measurement_time = L.measurement_time
  and M.failure_type = 'co2';

create or replace view Power_Off_Training_Data as
select T.* -- , L.maintenance_required
from reefer_telemetries T, labels L, data_gen_meta M
where
  T.container_id = M.container_id
  and L.container_id = T.container_id
  and T.measurement_time = L.measurement_time
  and M.failure_type = 'power';
"""

# Static SQL to load the products table
_LOAD_PRODUCTS_SQL = """
-- WARNING: DO NOT CHANGE THESE VALUES.
-- The data generator currently assumes that the target temperature
-- and humidity level for each product ID is EXACTLY as described here.
-- TODO: Modify the data generator so that it doesn't hard-code
-- these four products internally.
INSERT INTO products(product_id,
                     description,
                     target_temperature,
                     target_humidity_level)
VALUES
    ('P01','Carrots',4,0.4),
    ('P02','Banana',6,0.6),
    ('P03','Salad',4,0.4),
    ('P04','Avocado',6,0.4);
"""

################################################################################
# SUBROUTINES

def _bulk_load_table(cur: psycopg2.extensions.cursor,
                     df: pd.DataFrame,
                     df_cols: List[str],
                     table_name: str,
                     table_cols: List[str]):
    """
    Bulk load all the tuples in a dataframe into a table.

    Does not close out the current transaction.

    Raises any SQL-related errors thrown by the connection.

    Arguments:
        cur: Open cursor on an open connection to the DMBS
        df: Pandas dataframe of data to load
        df_cols: Names of columns in the dataframe to copy to the table
        table_name: Name of the table to append to. Must already exist.
        table_cols: Names of table columns that correspond to `df_cols`
    """
    # Round-trip through CSV format for now so we don't have to worry about
    # querying the SQL type info.
    csv_str = df[df_cols].to_csv(index=False, header=False)
    csv_buf = io.StringIO(csv_str)
    cur.copy_from(csv_buf, table_name, columns=(table_cols), sep=",")

def _sql_to_df(cur: psycopg2.extensions.cursor,
               query: str):
    """
    Execute a query and return the results as a dataframe.

    Args:
        cur: Open cursor on which to run the query
        query: SQL query string to execute

    Returns: Dataframe containing all columns of the query result in
    the order returned by the query.
    """
    cur.execute(query)
    result_tups = cur.fetchall()
    result_cols = [col.name for col in cur.description]
    return pd.DataFrame.from_records(result_tups,
                                     columns=result_cols)



def _get_product_meta(conn: psycopg2.extensions.connection):
    """
    Load the PRODUCTS table with an appropriate amount of dummy data, then
    retrieve all metadata about products from the database.

    Does NOT commit changes to the database. The caller should
    call `commit()` after all updates are in place, or `rollback()`
    if anything fails.

    Arguments:
        conn: Open connection to the database.

    Returns a dataframe with the same schema as the PRODUCTS table.
    """
    with conn.cursor() as cur:
        # Make this function idempotent.
        cur.execute("select count(*) from products")
        num_rows = cur.fetchone()[0]
        if 0 == num_rows:
            cur.execute(_LOAD_PRODUCTS_SQL)

        return _sql_to_df(cur, "select * from products")


def _get_container_meta(conn: psycopg2.extensions.connection,
                        product_meta: pd.DataFrame,
                        num_containers: int):
    """
    Load the REEFERS table with an appropriate amount of dummy data, then
    retrieve all metadata about containers from the database.

    Does NOT commit changes to the database. The caller should
    call `commit()` after all updates are in place, or `rollback()`
    if anything fails.

    Generates ID strings in the form "C####", where #### is a four-digit
    number.

    Also populates the "reefer_model" column.

    Arguments:
        conn: Open connection to the database.
        product_meta: The contents of the PRODUCTS table as a dataframe
        num_containers: Target number of rows for the REEFERS table

    Returns a dataframe with the following columns:
    * container_id: Serial number string for imaginary container
    * failure_type: String describing failure status of container;
                    can be 'none', 'co2', or 'power'
    * product_id: Product ID; references the PRODUCTS table
    """
    with conn.cursor() as cur:
        # Make this function idempotent
        cur.execute("select count(*) from reefers")
        num_rows = cur.fetchone()[0]
        num_to_generate = num_containers - num_rows
        # Add additional dummy containers as needed
        if num_to_generate > 0:
            if num_rows > 0:
                cur.execute("select max(container_id) from reefers")
                # ID is a string in the form 'Cxxxx', where xxxx is a number
                max_id = int(cur.fetchone()[0][1:])
            else:
                max_id = 0

            # Generate the concatenation of the REEFERS and
            ids = ["C{:04d}".format(i)
                   for i in range(max_id + 1, max_id + 1 + num_to_generate)]
            models = np.random.choice(_REEFER_MODELS, size=num_to_generate)
            product_ids = np.random.choice(product_meta.product_id,
                                           size=num_to_generate)
            failure_types = np.random.choice(["none", "co2", "power"],
                                             size=num_to_generate,
                                             p = [0.9, 0.05, 0.05])

            reefers_df = pd.DataFrame.from_dict({"container_id": ids,
                                                 "reefer_model": models})
            _bulk_load_table(cur, reefers_df, list(reefers_df.columns),
                             "reefers", list(reefers_df.columns))

            data_gen_meta_df = pd.DataFrame.from_dict(
                    { "container_id": ids,
                      "failure_type": failure_types,
                      "product_id" : product_ids })
            _bulk_load_table(cur, data_gen_meta_df,
                             list(data_gen_meta_df.columns),
                             "data_gen_meta",
                             list(data_gen_meta_df.columns))

        # All the columns we need are in the data_gen_meta table
        return _sql_to_df(cur, "select * from data_gen_meta")


def _gen_and_load(conn: psycopg2.extensions.connection,
                  container_id: str, failure_type: str,
                  product_id: str):
    """
    Generate and load some historical data for one container.

    Does NOT commit or abort the current transaction.  The caller should commit
    after loading all data or rollback if any part of the load fails.

    Raises any SQL-related exceptions thrown by the database interface.

    Arguments:
        conn: Open connection to the database.
        container_id: Unique ID string of the container
        failure_type: String encoding the failure state of the container;
            can be 'none', 'co2', or 'power'
        product_id: Product ID referencing the key of the PRODUCTS table.
    """
    data_gen = sim.ReeferSimulator()
    # Pick how far in the past the time series should start. We want the time
    # series end at a random point in the past 15 minutes.
    start_offset_hours = (_HOURS_PER_ROW * _ROWS_PER_CONTAINER
                          + np.random.uniform(0.0, _HOURS_PER_ROW))
    start_timestamp = (datetime.datetime.today()
                       - datetime.timedelta(hours=start_offset_hours))

    # Generate time series for the container
    if failure_type == "none":
        df = data_gen.generateNormalRecords(cid=container_id,
                                            nb_records=_ROWS_PER_CONTAINER,
                                            product_id=product_id,
                                            start_time=start_timestamp)
    elif failure_type == "co2":
        df = data_gen.generateCo2Records(cid=container_id,
                                         nb_records=_ROWS_PER_CONTAINER,
                                         product_id=product_id,
                                         start_time=start_timestamp)
    elif failure_type == "power":
        df = data_gen.generatePowerOffRecords(cid=container_id,
                                              nb_records=_ROWS_PER_CONTAINER,
                                              product_id=product_id,
                                              start_time=start_timestamp)
    else:
        raise ValueError("Can't handle failure type '{}'".format(failure_type))

    # Load the time series into the database
    col_names = list(df.columns)
    with conn.cursor() as cur:
        _bulk_load_table(cur, df, col_names, "reefer_telemetries", col_names)

        # Load training data table if required
        if failure_type != "none":
            col_names = ["container_id", "measurement_time",
                         "maintenance_required"]
            _bulk_load_table(cur, df,
                             df_cols=col_names,
                             table_name="labels",
                             table_cols=col_names)

# (dummy comment to work around vim bug)
def _get_env(var_name: str, default_value: Any):
    if var_name in os.environ:
        return os.environ[var_name]
    else:
        return default_value

################################################################################
# BEGIN SCRIPT

def main():
    # Read parameters from the environment
    server_ip = _get_env("LOAD_DB_POSTGRES_IP", None)
    server_port = _get_env("LOAD_DB_POSTGRES_PORT", None)
    db_name = _get_env("LOAD_DB_POSTGRES_DB", _DEFAULT_DB_NAME)
    user = _get_env("LOAD_DB_POSTGRES_USER", None)
    password = _get_env("LOAD_DB_POSTGRES_PASSWORD", None)

    with psycopg2.connect(host=server_ip,
                          port=server_port,
                          database=db_name,
                          user=user,
                          password=password) as conn:
        start_time = time.time()
        print("Creating internal tables")
        with conn.cursor() as cur:
            cur.execute(_CREATE_DDL)

        print("Generating PRODUCTS table")
        product_meta = _get_product_meta(conn)
        print("Products are:")
        print(product_meta)

        print("Generating REEFERS table")
        container_meta = _get_container_meta(conn, product_meta, _NUM_CONTAINERS)
        print("Container info:")
        print(container_meta)


        print("Generating REEFER_TELEMETRIES table")
        num_loaded = 0
        num_to_load = len(container_meta.index)
        for container_id, failure_type, product_id in container_meta.to_records(
                index=False):
            _gen_and_load(conn, container_id, failure_type, product_id)
            num_loaded = num_loaded + 1
            print("Loaded {} of {} time series...".format(num_loaded,
                  num_to_load), end="\r")

        # Save our changes.
        conn.commit()
        elapsed_time = time.time() - start_time
        print("Loaded {} time series into warehouse in {:.1f} sec."
              "".format(num_to_load, elapsed_time))

        # Can't run VACUUM command inside a transaction block, so put
        # the connection into autocommit mode.
        print("Updating optimizer statistics.")
        conn.set_session(autocommit=True)
        with conn.cursor() as cur:
            cur.execute("vacuum full freeze analyze")


if __name__ == "__main__":
    main()


