FROM python:3.7-slim

RUN pip3 install PyYaml exchange-metadata-converter==0.0.9

ENV APP_HOME /app
COPY src $APP_HOME
WORKDIR $APP_HOME

ENTRYPOINT ["python"]
CMD ["dataset_converter.py"]
