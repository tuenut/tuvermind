from __future__ import absolute_import, unicode_literals

import gzip
from json import loads

from celery import shared_task
from django.conf import settings

from apps.openweathermap.models import OWMCities
from libs.utils.network import GetDataByRequests


@shared_task
def get_cities_task():
    Cities().get()


class Cities:
    getter = GetDataByRequests()

    def get(self, ):
        self.getter.get_data(settings.URL_CITY_LIST)
        self.data = loads(gzip.decompress(self.getter.response.content))
        self.save(self.data)

    @staticmethod
    def save(data, ):
        for city in data:
            instance, created = OWMCities.objects \
                .get_or_create(owm_id=city['id'])
            instance.name = city['name']
            instance.country = city['country']
            instance.latitude = city['coord']['lat']
            instance.longitude = city['coord']['lon']
            instance.save()
