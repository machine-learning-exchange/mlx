FROM python:3.6-slim

RUN pip3 install kubernetes==10.0.1 requests==2.22.0

ENV APP_HOME /app
COPY src $APP_HOME
WORKDIR $APP_HOME

ENTRYPOINT ["python"]
CMD ["dataset_manager.py"]
