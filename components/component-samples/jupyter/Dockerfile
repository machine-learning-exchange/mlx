FROM python:3.7-slim AS base

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.7-slim AS build-image

COPY --from=base /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /jupyter

ADD src/* /jupyter/

ENTRYPOINT [ "python", "-u", "/jupyter/execute_notebook.py" ]
