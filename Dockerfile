FROM python:3.7-slim
MAINTAINER andrew.the.techie@gmail.com
LABEL description="Docker image for running errbot in kubernetes"

COPY ./errbot /errbot
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libssl-dev libffi-dev && \
    pip3 install --no-cache-dir -r /errbot/requirements.txt && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /errbot
CMD errbot -c config.py