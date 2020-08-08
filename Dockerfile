FROM python:3.8-slim
MAINTAINER andrew.the.techie@gmail.com
LABEL description="Docker image for running errbot in kubernetes, customized for the SA Devz"

COPY *requirements.txt /

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libssl-dev libffi-dev git&& \
    python -m venv /errbot/venv && \
    . /errbot/venv/bin/activate && \
    /errbot/venv/bin/pip install --no-cache-dir -r /requirements.txt && \
    /errbot/venv/bin/pip install --no-cache-dir -r /plugin-requirements.txt && \
    rm -rf /*requirements.txt && \
    rm -rf /var/lib/apt/lists/*
COPY ./errbot /errbot
WORKDIR /errbot

ENTRYPOINT ["/errbot/run.sh"]
