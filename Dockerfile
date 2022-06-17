FROM python:3.10-slim

EXPOSE 8000

RUN apt-get update -y && \
    apt-get install build-essential libpq-dev -y

COPY requirements.txt /tmp/requirements.txt

RUN python3 -m pip install pip --upgrade && \
    python3 -m pip install -r /tmp/requirements.txt

RUN useradd -m -s /bin/bash tuvermind
USER tuvermind

COPY --chown=tuvermind:tuvermind ./src/ /opt/tuvermind/

WORKDIR /opt/tuvermind/
