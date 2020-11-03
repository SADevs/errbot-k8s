FROM python:3.8-slim
MAINTAINER andrew.the.techie@gmail.com
LABEL description="Docker image for running errbot in kubernetes, customized for the SA Devz"

COPY *requirements.txt /

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libssl-dev libffi-dev git openssh-client gnupg software-properties-common && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-key C99B11DEB97541F0 && \
    apt-add-repository https://cli.github.com/packages && \
    apt-get update && \
    apt-get install gh && \
    python -m venv /errbot/venv && \
    . /errbot/venv/bin/activate && \
    /errbot/venv/bin/pip install --no-cache-dir -r /requirements.txt && \
    /errbot/venv/bin/pip install --no-cache-dir -r /plugin-requirements.txt && \
    install -d -o root -g root -m 0600 /root/.ssh && \
    apt-get autoremove --purge -y software-properties-common && \
    rm -rf /*requirements.txt && \
    rm -rf /var/lib/apt/lists/*
COPY ./errbot /errbot
WORKDIR /errbot

ENTRYPOINT ["bash", "/errbot/run.sh"]
