#!/usr/bin/env bash

celery -A web worker -E --loglevel=DEBUG
celery beat -A web --loglevel=INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler