FROM python:3.8-slim
MAINTAINER andrew.the.techie@gmail.com
LABEL description="Docker image for running errbot in kubernetes, customized for the SA Devz"

COPY ./errbot /errbot
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libssl-dev libffi-dev && \
    python -m venv /errbot/venv && \
    . /errbot/venv/bin/activate && \
    /errbot/venv/bin/pip install --no-cache-dir -r /errbot/requirements.txt && \
    /errbot/venv/bin/pip install --no-cache-dir -r /errbot/plugin-requirements.txt && \
    rm -rf /errbot/*requirements.txt && \
    rm -rf /var/lib/apt/lists/* && \
    chmod +x /errbot/run.sh

WORKDIR /errbot

ENTRYPOINT ["/errbot/run.sh"]
