#!/bin/bash

celery beat -A apps --loglevel=INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
