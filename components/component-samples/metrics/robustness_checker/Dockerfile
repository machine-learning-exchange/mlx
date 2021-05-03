FROM pytorch/pytorch:latest

RUN pip install adversarial-robustness-toolbox Flask pandas minio flask-cors Pillow torchsummary

ENV APP_HOME /app
COPY src $APP_HOME
WORKDIR $APP_HOME

ENTRYPOINT ["python"]
CMD ["app.py"]
