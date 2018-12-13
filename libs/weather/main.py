import wget


from datetime import datetime as dt
from json import loads
from libs.weather.config import (ICONS, OPENWAETHERMAP_URL, ICONS_PATH,
                                 MAX_WIDTH, ICON_WIDTH, SYMBOL_H, SYMBOL_W,
                                 ALIGN, HOURS_TO_DISPLAY,)


def get_icons():
    for icon in ICONS:
        wget.download(OPENWAETHERMAP_URL+icon, out=ICONS_PATH+icon)


class ParseWeatherData:
    pass

    def __init__(self):
        self.weather_data = {}
        self.conky_text = ''

    def parse(self, curl_json_response):
        weather_data = loads(curl_json_response)
        self.weather_data = {}
        for item in weather_data['list']:
            date = dt.utcfromtimestamp(item['dt'])
            temp = round(item['main']['temp'] - 273.0, 2)  # C
            pressure = item['main']['pressure']  # hPa
            humidity = item['main']['humidity']  # %
            cloudiness = item['clouds']['all']  # %
            weather = list(item['weather'][0].values())
            wind = item['wind']
            by_time = {
                date.strftime('%H:%M'): {
                    'temp': temp,
                    'pressure': pressure,
                    'humidity': humidity,
                    'cloudiness': cloudiness,
                    'weather': weather,
                    'wind': wind
                }
            }
            try:
                self.weather_data[date.date()].update(by_time)
            except KeyError:
                self.weather_data[date.date()] = by_time


class ProcessWeatherData:
    IMG_PATTERN = '${{image /home/tuenut/.conky/weather_icons/{img}.png -p {x:0.0f},{y:0.0f}}}'

    def __init__(self):
        self.weather_data = {}
        self.conky_text = ''

    def text_prepare(self, days):
        text = ''
        sorted_days = sorted(days)

        for day in sorted_days:
            if sorted_days.index(day) == 0:
                sorted_hours = sorted(days[day])[:3]
            else:
                sorted_hours = [hour for hour in sorted(days[day]) if
                                hour in HOURS_TO_DISPLAY]
            times = ''.join([
                '{:^{align}}'.format('{:<10}'.format(hour),
                                     align=ALIGN)
                for hour in sorted_hours
            ])
            temps = ''.join([
                '{:^{align}}'.format(
                    '{:>10}'.format(
                        '{: .2f}C°'.format(days[day][hour]['temp'])),
                    align=ALIGN)
                for hour in sorted_hours
            ])
            pressures = ''.join([
                '{:^{align}}'.format(
                    '{:>9.02f}мм'.format(
                        float(days[day][hour]['pressure']) / 1.3),
                    align=ALIGN)
                for hour in sorted_hours
            ])
            humidityes = ''.join([
                '{:^{align}}'.format(
                    '{:>5}'.format(float(days[day][hour]['humidity'])),
                    align=ALIGN)
                for hour in sorted_hours
            ])
            cloudinesses = ''.join([
                '{:^{align}}'.format(
                    '{:>5}'.format(float(days[day][hour]['cloudiness'])),
                    align=ALIGN)
                for hour in sorted_hours
            ])
            wind = ''.join([
                '{:^{align}}'.format(
                    '{:>8}м/с'.format(float(days[day][hour]['wind']['speed'])),
                    align=ALIGN)
                for hour in sorted_hours
            ])
            images = ''.join([
                self.IMG_PATTERN.format(
                    img=days[day][hour]['weather'][-1],
                    x=40 + ALIGN * SYMBOL_W * (sorted_hours.index(hour)),
                    y=26 + (SYMBOL_H * 4 + 24) * (sorted_days.index(day)),
                )
                for hour in sorted_hours
            ])
            text += '''\
${{offset 20}}${{alignc}}${{font Terminus:bold:24}}${{color5}}{day}${{color}}${{font}}
${{offset 40}}${{alignc}}${{color5}}{hours}${{color}}
${{offset 40}}${{alignc}}{temps}
${{offset 40}}${{alignc}}{wind}
{images}${{color1}}${{hr 2}}\n'''.format(
                day=day,
                hours=times,
                temps=temps,
                wind=wind,
                images=images
            )
            text = text.replace('${alignc}', '')