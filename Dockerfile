FROM python:3.10-slim

EXPOSE 8000

RUN useradd -m -s /bin/bash tuvermind

RUN  mkdir -p \
     /var/www/tuvermind/media \
     /var/www/tuvermind/static \
     /var/log/tuvermind/ \
     /opt/tuvermind/ \
RUN chown tuvermind:tuvermind \
     /var/www/tuvermind/media \
     /var/www/tuvermind/static \
     /var/log/tuvermind/ \
     /opt/tuvermind/ \

COPY requirements.txt /tmp/requirements.txt
RUN apt-get update -y && \
    apt-get install build-essential libpq-dev -y
RUN python3 -m pip install pip --upgrade && \
    python3 -m pip install -r /tmp/requirements.txt

USER tuvermind
COPY ./src/ /opt/tuvermind/
WORKDIR /opt/tuvermind/
