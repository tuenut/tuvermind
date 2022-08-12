from __future__ import absolute_import, unicode_literals

from datetime import datetime as dt
from io import BytesIO
from json import loads

from celery import shared_task
from django.utils import timezone
from django.conf import settings

from apps.openweathermap.models import OWMCities, OWMData, OWMWeather
from libs.utils.network import GetDataByRequests


@shared_task
def get_weather_task():
    weather_getter = Weather()
    data = weather_getter.get()
    weather_getter.save(data)


class Weather:
    getter = GetDataByRequests()
    _now: dt

    def get(self):
        self.getter.get_data(settings.URL_FORECAST_5_DAYS)
        return loads(self.getter.response.text)

    def save(self, data):
        self._now = timezone.now()
        city = self._get_city(data)

        for owm_response_data in data['list']:
            self._save_weather(city, owm_response_data)

    def _save_weather(self, city, data):
        weather_data, _ = OWMData.objects.get_or_create(
            timestamp=self._parse_timestamp(data),
            city=city
        )

        self._set_weather_data(weather_data, data)
        self._set_weather(weather_data, data['weather'][0])
        self._set_precipitation(weather_data, data)

        weather_data.save()

    def _get_city(self, data: dict):
        try:
            city = OWMCities.objects.get(owm_id=data['city']['id'])
        except OWMCities.DoesNotExist:
            city = OWMCities.create_new_city_from_owm_data(data['city'])

        return city

    def _set_weather_data(self, weather_data: OWMData, response_data: dict):
        weather_data.updated = self._now
        weather_data.temperature = response_data['main']['temp']
        weather_data.temperature_min = response_data['main']['temp_min']
        weather_data.temperature_max = response_data['main']['temp_max']
        weather_data.pressure = response_data['main']['pressure']
        weather_data.humidity = response_data['main']['humidity']
        weather_data.clouds = response_data['clouds']['all']
        weather_data.wind_speed = response_data['wind']['speed']
        weather_data.wind_deg = response_data['wind']['deg']

    def _parse_timestamp(self, response_data: dict):
        timestamp = response_data['dt']
        timestamp = dt.utcfromtimestamp(timestamp)
        return timezone.make_aware(timestamp)

    def _set_precipitation(self, weather_data: OWMData, response_data: dict):
        try:
            weather_data.snow_3h = response_data['snow']['3h']
        except KeyError:
            weather_data.snow_3h = None
        try:
            weather_data.rain_3h = response_data['rain']['3h']
        except KeyError:
            weather_data.rain_3h = None

    def _set_weather(self, weather_data: OWMData, response_data: dict):
        try:
            weather_data.weather = OWMWeather.objects.get(
                owm_id=response_data['id'])
        except OWMWeather.DoesNotExist:
            self._create_new_weather(response_data)

    def _create_new_weather(self, weather):
        weather_instance, created = OWMWeather.objects.get_or_create(
            owm_id=weather['id'],
            name=weather['main'],
            description=weather['description'],
        )

        if not weather_instance.icon:
            icon_file = self._get_weather_icon(weather["icon"])
            self._attach_icon(weather_instance, weather["icon"], icon_file)

    def _get_weather_icon(self, icon):
        self.getter.get_data(settings.URL_IMAGE_PREFIX % icon)
        return BytesIO(self.getter.response.content)

    def _attach_icon(self, weather_instance, icon, file):
        weather_instance.icon.save(icon, file)
        weather_instance.save()
