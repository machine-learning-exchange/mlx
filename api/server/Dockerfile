FROM python:3.9-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

# https://stackoverflow.com/questions/66118337/how-to-get-rid-of-cryptography-build-error
# ENV CRYPTOGRAPHY_DONT_BUILD_RUST 1
# apk add gcc musl-dev python3-dev libffi-dev openssl-dev cargo

RUN apk add --update --virtual build-dependencies \
        pkgconfig \
        openssl-dev \
        libffi-dev \
        musl-dev \
        make \
        gcc \
        g++ \
        curl \
        cargo \
    && apk add --update git \
    && curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl \
    && chmod +x kubectl \
    && mv kubectl /usr/local/bin \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apk del --purge build-dependencies \
    && rm -rf \
        /var/cache/apk/* \
        /root/.cache \
        /tmp/*

RUN pip list

COPY . /usr/src/app

RUN ls */*

EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["-m", "swagger_server"]
