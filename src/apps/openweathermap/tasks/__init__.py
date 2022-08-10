from __future__ import absolute_import, unicode_literals

from celery import shared_task

from libs.utils.network import GetDataByRequests
from settings.openweathermap import URL_FORECAST_5_DAYS
from apps.openweathermap.tasks.lib import Weather, Cities


@shared_task
def test_task():
    a = GetDataByRequests()
    a.get_data(URL_FORECAST_5_DAYS)
    a.log_data()


@shared_task
def get_weather_task():
    Weather().get()


@shared_task
def get_cities_task():
    Cities().get()
