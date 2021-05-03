FROM python:3.6-slim

ENV KFP_PACKAGE=https://storage.googleapis.com/ml-pipeline/release/0.1.8/kfp.tar.gz

RUN pip install ruamel.yaml requests
RUN pip install $KFP_PACKAGE

ENV APP_HOME /app
COPY src $APP_HOME
WORKDIR $APP_HOME
