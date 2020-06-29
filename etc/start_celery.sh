#!/bin/bash

celery -A apps worker -E --loglevel=DEBUG
