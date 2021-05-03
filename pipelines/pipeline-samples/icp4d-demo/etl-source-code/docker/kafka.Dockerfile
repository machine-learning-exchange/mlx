
# Dockerfile for building the "toy Kafka server" job
# To build the image from root of the project, type:
#   wget
#   http://www.gtlib.gatech.edu/pub/apache/kafka/2.3.0/kafka_2.12-2.3.0.tgz \
#       --output-document=docker/kafka_2.12-2.3.0.tgz
#   docker build . --file docker/kafka.Dockerfile --tag frreiss/kafka
#
# To run a local Kafka server from this image:
#   docker run -it -p 9092:9092 frreiss/kafka
# (note the "-it" argument, which lets you stop the server with control-C)
#
# To run an interactive shell inside this image:
#   docker run -it --entrypoint /bin/bash frreiss/kafka

# Any stable Ubuntu release should do
FROM ubuntu:latest
RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get install -y \
        default-jre \
        wget

# Copy our install script into the image, create an output directory,
# and run the script.
COPY scripts/install_kafka.sh scripts/start_kafka_docker.sh /
ENV KAFKA_BASE /usr/local/kafka
ENV KAFKA_LISTEN_HOST "0.0.0.0"
RUN mkdir ${KAFKA_BASE}
# Script downloads the file if not present. Use an COPY command so that the
# output of "docker build" looks cleaner.
COPY docker/kafka_2.12-2.3.0.tgz ${KAFKA_BASE}
RUN /install_kafka.sh

CMD /start_kafka_docker.sh
EXPOSE 9092

