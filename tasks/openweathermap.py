from __future__ import absolute_import, unicode_literals

from celery import shared_task

from libs.openweathermap import get_weather

@shared_task
def get_weather_task():
    get_weather()