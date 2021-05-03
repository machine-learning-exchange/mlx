
# Dockerfile for building the ETL PySpark job
# To build the image from root of the project, type:
#   docker build . --file docker/etl.Dockerfile --tag frreiss/etl
#
# To run the main ETL script from this image:
# 
#   docker run frreiss/etl python /etl.py \
#       --kafka_bootstrap_servers $KAFKA_BOOTSTRAP_SERVERS \
#       --kafka_topic $KAFKA_TOPIC \
#       --postgres_host $POSTGRES_HOST \
#       --postgres_port $POSTGRES_PORT \
#       --postgres_user $POSTGRES_USER \
#       --postgres_password $POSTGRES_PASSWORD \
#       --postgres_db $POSTGRES_DB
# (where KAFKA_BOOTSTRAP_SERVERS and so on are environment variables or string
# literals with the appropriate parameter values)
#
# To run a script that pushes some records to Kafka:
#   docker run frreiss/etl python /push.py \
#       --kafka_bootstrap_servers $KAFKA_BOOTSTRAP_SERVERS \
#       --kafka_topic $KAFKA_TOPIC \
#       [--container_id <ID>]
#       [--num_records <NUM>]
#       [--record_type <'normal'|'co2'|'power'>]
#
# (arguments in square brackets are optional)
#   
# To run an interactive shell inside this image:
#   docker run -it --entrypoint /bin/bash frreiss/etl

# Miniconda base image so we have an easy way to install a working pyspark
FROM continuumio/miniconda3
RUN apt-get update && apt-get -y upgrade

# PySpark requires Java 8 (!) 
# Java package in the base image depends on a package that is broken. Here's a
# workaround for the broken package:
RUN mkdir -p /usr/share/man/man1
# Now we can install Java
# Or not; Java 8 is hard to get on Debian. So we use conda to install it below.
#RUN apt-get update && apt-get install -y default-jdk

# Install all the Python libraries we need to run the script.
RUN conda update -n base -c defaults conda
RUN conda create -n env python=3.6 \
    numpy \
    pandas \
    psycopg2 \
    pyspark=2.4.0 
    
RUN conda install -n env -y -c conda-forge python-confluent-kafka pyarrow=0.10.0

# Here's where we install Java 8 with conda. Remove this once Spark supports a
# modern version of Java.
RUN conda install -n env -y openjdk

RUN echo "source activate env" >> ~/.bashrc
ENV PATH /opt/conda/envs/env/bin:$PATH

# Copy in the ETL script's files.
COPY scripts/etl.py scripts/etl_lib.py /

# Copy in additional files so we can also run the "push data to Kafka" script 
# from this image.
COPY scripts/push.py /
COPY reefer /reefer

