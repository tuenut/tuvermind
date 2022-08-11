import os

from .environment import API_KEY

__all__ = [
    "URL_FORECAST_5_DAYS", "URL_CITY_LIST", "HOURS_TO_DISPLAY",
    "URL_IMAGE_PREFIX",
]

URL_FORECAST_5_DAYS = \
    f"https://api.openweathermap.org/data/2.5/forecast" \
    f"?q=bryansk,RU&appid={API_KEY}"
URL_CITY_LIST = "https://bulk.openweathermap.org/sample/city.list.json.gz"
URL_IMAGE_PREFIX = "https://openweathermap.org/img/w/%s.png"

HOURS_TO_DISPLAY = ["06:00", "12:00", "18:00"]
ICONS = {
    "01d.png": "clear sky",
    "01n.png": "clear sky",
    "02d.png": "few clouds",
    "02n.png": "few clouds",
    "03d.png": "scattered clouds",
    "03n.png": "scattered clouds",
    "04d.png": "broken clouds",
    "04n.png": "broken clouds",
    "09d.png": "shower rain",
    "09n.png": "shower rain",
    "10d.png": "rain",
    "10n.png": "rain",
    "11d.png": "thunderstorm",
    "11n.png": "thunderstorm",
    "13d.png": "snow",
    "13n.png": "snow",
    "50d.png": "mist",
    "50n.png": "mist",
}
