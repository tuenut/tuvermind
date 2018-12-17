import os

API_KEY = 'c8ac975c083a2ece2e838496b1d0f7af'
URL = 'http://api.openweathermap.org/data/2.5/forecast?q=bryansk,RU&appid=%s' % API_KEY
OPENWAETHERMAP_URL = 'http://openweathermap.org/img/w/'
PATH = os.path.expanduser('~/.conky/openweathermap/')
ICONS_PATH = os.path.join(PATH, 'icons')
ICONS = {
    '01d.png': 'clear sky',
    '01n.png': 'clear sky',
    '02d.png': 'few clouds',
    '02n.png': 'few clouds',
    '03d.png': 'scattered clouds',
    '03n.png': 'scattered clouds',
    '04d.png': 'broken clouds',
    '04n.png': 'broken clouds',
    '09d.png': 'shower rain',
    '09n.png': 'shower rain',
    '10d.png': 'rain',
    '10n.png': 'rain',
    '11d.png': 'thunderstorm',
    '11n.png': 'thunderstorm',
    '13d.png': 'snow',
    '13n.png': 'snow',
    '50d.png': 'mist',
    '50n.png': 'mist',
}

# conky
MAX_WIDTH = 1200
ICON_WIDTH = 50
SYMBOL_W = 8
SYMBOL_H = 14
ALIGN = 20
HOURS_TO_DISPLAY = ['06:00', '12:00', '18:00', ]