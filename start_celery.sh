#!/usr/bin/env bash

celery -A web worker -E --loglevel=DEBUG
