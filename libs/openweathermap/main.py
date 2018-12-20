import gzip

from datetime import datetime as dt
from json import loads
from io import BytesIO

from django.utils import timezone

from libs.openweathermap.config import (URL_IMAGE_PREFIX, SYMBOL_H, PATH, SYMBOL_W, ALIGN, HOURS_TO_DISPLAY,
                                        URL_FORECAST_5_DAYS, URL_CITY_LIST)
from libs.utils.network import GetDataByRequests
from libs.utils.logger import Logger
from web.apps.openweathermap.models import OWMCities, OWMData, OWMWeather


class Weather(metaclass=Logger):
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
            instance, created = OWMData.objects.get_or_create(timestamp=timestamp, city=city)
            instance.updated = timezone.now()

            instance.temperature = item['main']['temp']
            instance.temperature_min = item['main']['temp_min']
            instance.temperature_max = item['main']['temp_max']
            instance.pressure = item['main']['pressure']
            instance.humidity = item['main']['humidity']

            #Get weather instance or create if not exist.
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


class Cities(metaclass=Logger):
    getter = GetDataByRequests()

    def get(self, ):
        self.getter.get_data(URL_CITY_LIST)
        self.data = loads(gzip.decompress(self.getter.response.content))
        self.save(self.data)

    @staticmethod
    def save(data, ):
        for city in data:
            instance, created = OWMCities.objects.get_or_create(owm_id=city['id'])
            instance.name = city['name']
            instance.country = city['country']
            instance.latitude = city['coord']['lat']
            instance.longitude = city['coord']['lon']
            instance.save()



class UpdateConkyConfig(metaclass=Logger):
    def __init__(self):
        self.get()
        self.process()

    def get(self):
        # запрос погоды из базы
        data = OWMData.objects.filter(timestamp__gte=timezone.now() - timezone.timedelta(hours=3))
        self.data = {}
        for obj in data:
            hourly_weather = {
                'temperature': obj.temperature,
                'wind_speed': obj.wind_speed,
                'icon': obj.weather.icon.file
            }
            date = obj.timestamp.strftime('%Y-%m-%d')
            hour = obj.timestamp.strftime('%H:%M')
            try:
                self.data[date].update({hour: hourly_weather})
            except KeyError:
                self.data[obj.timestamp.strftime('%Y-%m-%d')] = {hour: hourly_weather}

    def process(self):
        # обработка и генеарция текста для conky
        day_line_pattern = '${{offset 20}}${{font Terminus:bold:24}}${{color5}}{}${{color}}${{font}}'

        hours_1st_pattern = '{:^{align}}'
        hours_2nd_pattern = '{:>10}'
        hours_line_pattern = '${{offset 40}}${{color5}}{}${{color}}'

        temp_1st_pattern = '{:^{align}}'
        temp_2nd_pattern = '{:>10}'
        temp_line_pattern = '${{offset 40}}{}'

        wind_1st_pattern = '{:^{align}}'
        wind_2nd_pattern = '{:>10}'
        wind_line_pattern = '${{offset 40}}{}'

        icons_1st_pattern = '${{image {} -p {x:0.0f},{y:0.0f}}}'
        icons_line_pattern = '{}${{color1}}${{hr 2}}\n'

        sorted_days = sorted(self.data)

        text = ''

        def construct_text(data=None, pattrn_one='{}', pattern_two='{}', pattern_line='{}', **kwargs):
            if not data:
                return False
            text_list = [pattrn_one.format(pattern_two.format(item, **kwargs), **kwargs) for item in data]
            line = pattern_line.format(''.join(text_list), **kwargs)
            return line

        for day in sorted_days:
            sorted_hours = [hour for hour in sorted(self.data[day]) if hour in HOURS_TO_DISPLAY]
            weather = self.data[day]
            day_text = day_line_pattern.format(day)

            hours = construct_text(
                data=sorted_hours,
                pattrn_one=hours_1st_pattern,
                pattern_two=hours_2nd_pattern,
                pattern_line=hours_line_pattern,
                align=ALIGN
            )

            temp = ['{: .2f}C°'.format(weather[key]['temperature'] - 273.0) for key in sorted_hours]
            temp = construct_text(
                data=temp,
                pattrn_one=temp_1st_pattern,
                pattern_two=temp_2nd_pattern,
                pattern_line=temp_line_pattern,
                align=ALIGN
            )

            wind = ['{: .2f}м/с'.format(weather[key]['wind_speed']) for key in sorted_hours]
            wind = construct_text(data=wind,
                pattrn_one=wind_1st_pattern,
                pattern_two=wind_2nd_pattern,
                pattern_line=wind_line_pattern,
                align=ALIGN
            )

            icons = [
                icons_1st_pattern.format(weather[hour]['icon'],
                                         x=40 + ALIGN * SYMBOL_W * (sorted_hours.index(hour)),
                                         y=26 + (SYMBOL_H * 4 + 24) * (sorted_days.index(day)), )
                for hour in sorted_hours
            ]
            icons = ''.join(icons)
            icons = icons_line_pattern.format(icons)

            text += '\n'.join([day_text, hours, temp, wind, icons])

        with open(PATH + 'weather_part', 'w') as f:
            f.write(text)
