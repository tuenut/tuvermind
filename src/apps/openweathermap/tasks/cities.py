from __future__ import absolute_import, unicode_literals

import gzip
from json import loads

from celery import shared_task
from django.conf import settings

from apps.openweathermap.models import OWMCities
from libs.utils.network import GetDataByRequests


@shared_task
def get_cities_task():
    cities_getter = Cities()
    data = cities_getter.get()
    cities_getter.save(data)


class Cities:
    getter = GetDataByRequests()

    def get(self, ):
        self.getter.get_data(settings.URL_CITY_LIST)
        return loads(gzip.decompress(self.getter.response.content))

    @staticmethod
    def save(data, ):
        for city in data:
            OWMCities.create_new_city_from_owm_data(city)
