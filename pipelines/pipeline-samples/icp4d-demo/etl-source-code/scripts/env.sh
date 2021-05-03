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
# env.sh
#
# Set up a Python environment for running the demo.
#
# Requires that conda be installed and set up for calling from bash scripts.
#
# Also requires that you set the environment variable CONDA_HOME to the
# location of the root of your anaconda/miniconda distribution.
################################################################################

PYTHON_VERSION=3.7

ENV_DIR="./env"

############################
# HACK ALERT *** HACK ALERT
# The friendly folks at Anaconda thought it would be a good idea to make the
# "conda" command a shell function.
# See https://github.com/conda/conda/issues/7126
# The following workaround will probably be fragile.
if [ -z "$CONDA_HOME" ]
then
    echo "Error: CONDA_HOME not set"
    exit
fi
. ${CONDA_HOME}/etc/profile.d/conda.sh
# END HACK
############################


# Remove the detrius of any previous runs of this script
if ([ -a ${ENV_DIR} ])
then
    rm -rf ${ENV_DIR}
fi


# Create initial env with official prereqs for running tests
conda create -y --prefix ${ENV_DIR} \
    python=${PYTHON_VERSION} \
    jupyterlab \
    matplotlib \
    numpy \
    postgresql \
    psycopg2 \
    pyarrow \
    pyspark \
    scipy \
    scikit-learn \
    wheel \


conda activate ${ENV_DIR}

# Install conda-forge packages
conda install -y -c conda-forge python-confluent-kafka
conda install -y -c conda-forge kfp

# pip-based package installs go here
pip install hmmlearn

conda deactivate

echo << EOM
Anaconda environment created at ${ENV_DIR}. To activate, type:
   conda activate ${ENV_DIR}
EOM



