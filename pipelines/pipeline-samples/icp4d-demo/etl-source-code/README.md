# jupyterdemo

Demo application showing the processing of telemetry data using an open-source toolchain.

### Subdirectores 

* **scripts**: Various top-level driver scripts. See the comment at the top of each script for more info.
* **docs**: Directory that will eventually hold documentation. Currently not
  used.
* **notebooks**: Jupyter notebooks for components of the demonstration
  scenario.

### Getting started: Local, non-containerized

1. Install prerequisites:
   * Anaconda or Miniconda should be installed
   * The environment varialbe `CONDA_HOME` should be set to the location of
     your anaconda/miniconda install (for example, `${HOME}/miniconda3`, for a
     Mac install of Miniconda with Python 3)
1. Clone Fred's fork of the reference architecture project into this directory:
   ```
   git clone https://github.com/frreiss/reefer.git
   cd reefer
   git checkout datagen
   cd ..
   ```
1. Run the script `./scripts/env.sh` to create the Anaconda environment `./env`
1. `conda activate ./env`
1. Run the script `./scripts/create_db.sh` to create the local Postgres database
1. Run 
   ```PYTHONPATH=$PWD python ./scripts/load_db.py``` 
   to load an initial set of records into the local Postgres database
1. Run `jupyter lab` to fire up a Jupyter environment
1. TODO: More instructions

### Getting started: Kubernetes/OpenShift

TODO: Instructions go here


### Running the ETL script: Local, non-containerized

1. Follow the instructions above under "Getting started: Local".
   In particular, your local copy of the repository should be in a state where
   an Anaconda environment exists under `./env` and is active; PostgreSQL is 
   installed and started; you have created and loaded the database; and
   JupyterLab is running.
1. Download some Kafka binaries by running the script:
   ```scripts/install_kafka.sh```
1. Start up local Kafka and Zookeeper servers by running the script:
   ```scripts/start_kafka.sh```
1. (optional) Use the script
   `env/kafka_2.12-2.3.0/bin/kafka-console-consumer.sh` to monitor the Kafka
   topic `reefer`.
1. Open up the Jupyter notebook `notebooks/push.ipynb`. Whenever this notebook
   runs, it pushes 10 records to the `reefer` topic on the local Kafka server.
   If you're monitoring the `reefer` Kafka topic, you should see JSON data on
   that topic.
1. Run the ETL job. There are two ways to do this:
   a. Use the notebook `notebooks/ETL.ipynb`
   b. Use the script `scripts/etl.py`
   If you're looking at the database (say, with `psql`) you should see new rows 
   inserted into the database as a result of the ETL job.
1. (optional) Push more records into the channel by rerunning `push.ipynb` and
   run ETL a second time.
1. When you're done using Kafka, shut down Kafka and Zookeeper by running the
   script:
   ```scripts/stop_kafka.sh```


### Running the ETL script: Kubernetes/OpenShift

TODO: Instructions go here

