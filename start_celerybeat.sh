#!/usr/bin/env bash

celery beat -A web --loglevel=INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
