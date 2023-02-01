FROM python:3.10-alpine as builder

COPY ./requirements.txt /tmp/requirements.txt

RUN apk add --no-cache  \
      python3-dev  \
      gcc  \
      musl-dev  \
      linux-headers && \
    python3 -m pip install --upgrade pip && \
    python3 -m pip install --user uwsgi && \
    python3 -m pip install --user -r /tmp/requirements.txt

FROM python:3.10-alpine as app

EXPOSE 8000
ENV PATH=$PATH:/home/tuvermind/.local/bin \
    TUVERMIND_DEBUG=false \
    TUVERMIND_SECRET_KEY=secret_key \
    TUVERMIND_API_KEY=api_key \
    TUVERMIND_REDIS_HOST=redis \
    TUVERMIND_REDIS_PORT=6379 \
    TUVERMIND_DB_USER=db_user \
    TUVERMIND_DB_PASSWORD=db_password \
    TUVERMIND_DB_HOST=db_host \
    TUVERMIND_DB_PORT=5432


RUN addgroup tuvermind -g 11000 && \
    adduser -h /home/tuvermind/ -G tuvermind -u 11000 tuvermind -D && \
    mkdir -p "/home/tuvermind/logs/" && \
    chown tuvermind:tuvermind /home/tuvermind/logs/

COPY --from=builder --chown=tuvermind:tuvermind /root/.local/ /home/tuvermind/.local/
COPY --chown=tuvermind:tuvermind ./src/ /home/tuvermind/app/

USER tuvermind
WORKDIR /home/tuvermind/app/

