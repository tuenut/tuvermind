import gzip

from datetime import datetime as dt
from json import loads
from io import BytesIO

from django.utils import timezone

from settings.openweathermap import URL_IMAGE_PREFIX, URL_FORECAST_5_DAYS, \
    URL_CITY_LIST
from libs.utils.network import GetDataByRequests
from apps.openweathermap.models import OWMCities, OWMData, OWMWeather


class Weather:
    getter = GetDataByRequests()

    def get(self, ):
        self.getter.get_data(URL_FORECAST_5_DAYS)
        self.data = loads(self.getter.response.text)
        self.save()

    def save(self, ):
        # Get city instance or create if not exist.
        try:
            city = OWMCities.objects.get(owm_id=self.data['city']['id'])
        except OWMCities.DoesNotExist:
            Cities.save([self.data['city'], ])
            city = OWMCities.objects.get(owm_id=self.data['city']['id'])

        for item in self.data['list']:
            weather = item['weather'][0]
            timestamp = timezone.make_aware(dt.utcfromtimestamp(item['dt']))
            instance, created = OWMData.objects.get_or_create(
                timestamp=timestamp, city=city)
            instance.updated = timezone.now()

            instance.temperature = item['main']['temp']
            instance.temperature_min = item['main']['temp_min']
            instance.temperature_max = item['main']['temp_max']
            instance.pressure = item['main']['pressure']
            instance.humidity = item['main']['humidity']

            # Get weather instance or create if not exist.
            try:
                instance.weather = OWMWeather.objects.get(owm_id=weather['id'])
            except OWMWeather.DoesNotExist:
                weather_instance, created = OWMWeather.objects.get_or_create(
                    owm_id=weather['id'],
                    name=weather['main'],
                    description=weather['description'],
                )

                if not weather_instance.icon:
                    # Download icon.
                    self.getter.get_data(URL_IMAGE_PREFIX % weather['icon'])
                    icon_file = BytesIO(self.getter.response.content)

                    weather_instance.icon.save(weather['icon'], icon_file)
                    weather_instance.save()

            instance.clouds = item['clouds']['all']
            instance.wind_speed = item['wind']['speed']
            instance.wind_deg = item['wind']['deg']

            try:
                instance.snow_3h = item['snow']['3h']
            except KeyError:
                instance.snow_3h = None
            try:
                instance.rain_3h = item['rain']['3h']
            except KeyError:
                instance.rain_3h = None

            instance.save()


class Cities:
    getter = GetDataByRequests()

    def get(self, ):
        self.getter.get_data(URL_CITY_LIST)
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
