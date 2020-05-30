#!/bin/bash

celery -A web worker -E --loglevel=DEBUG
