FROM python:3.6-slim

RUN apt-get update
RUN apt-get install -y curl gnupg
RUN apt-get install -y apt-transport-https

RUN pip install kubernetes Flask flask-cors requests ruamel.yaml

ENV APP_HOME /app
COPY src $APP_HOME
WORKDIR $APP_HOME

ENTRYPOINT ["python"]
CMD ["app.py"]
