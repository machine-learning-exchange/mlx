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
# create_db.sh
#
# [re]create the initial state of the local development Postgres database for
# the demo.
#
# Does NOT load the tables of the database. Use load_db.py for that.
#
# Requires that you have already run env.sh and activated the resulting
# environment.
#
# Must be run from the root of the project.
################################################################################

function status {
    echo "*********** ${1}"
}

# The rest of this script depends on the conda environment's PostgreSQL
# install
ENV_DIR="${PWD}/env"
if ([ "${CONDA_DEFAULT_ENV}" != "${ENV_DIR}" ])
then
    echo "Error: Conda enviornment at ${ENV_DIR} not activated"
    exit
fi


DB_DIR="./dbms"
LOGFILE="./dbms.log"
DB_NAME="demo"

# Clean out any existing copy of the database
if ([ -a $DB_DIR ])
then
    status "Removing previous copy of database"
    pg_ctl -D $DB_DIR stop
    rm -rf $DB_DIR
    rm -f $LOGFILE
fi

status "Initializing Postgres data directory; this may take a while."
mkdir $DB_DIR
initdb -D $DB_DIR
pg_ctl -D $DB_DIR -l $LOGFILE start

status "Creating database '${DB_NAME}'."
createdb $DB_NAME
psql --dbname=${DB_NAME} --file=./reefer/postgresql/createTables.sql
#psql --dbname=${DB_NAME} --file=./scripts/create_tables.sql
#
#status "Populating small tables in database '${DB_NAME}'."
#psql --dbname=${DB_NAME} --file=./scripts/populate_tables.sql
#
#status "Generating large tables in database '${DB_NAME}'"
#PYTHONPATH=$PWD python3 scripts/load_db.py

status "Database server started on localhost."
echo "To shut down, run:"
echo "pg_ctl -D ${DB_DIR} stop"
echo ""
echo "To open a SQL console, run:"
echo "psql --dbname=${DB_NAME}"

