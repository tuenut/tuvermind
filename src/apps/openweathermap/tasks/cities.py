from __future__ import absolute_import, unicode_literals

import gzip
from json import loads

from loguru import logger

from celery import shared_task
from django.conf import settings

from apps.openweathermap.models import OWMCities
from libs.tasks.bases import LoggedTask
from libs.utils.network import GetDataByRequests


@shared_task(base=LoggedTask, name="Get OWM cities")
def get_cities_task():
    getter = GetDataByRequests()

    logger.debug(f"Start getting data from OWM...")
    response = getter.get_data(settings.URL_CITY_LIST)
    logger.debug(f"Ok.")

    logger.debug(f"Decompressing data...")
    data = loads(gzip.decompress(response.content))
    logger.debug("Ok.")

    logger.debug(f"Start saving data to db...")
    for city in data:
        OWMCities.update_city_data(city)

    logger.debug(f"All data saved.")
