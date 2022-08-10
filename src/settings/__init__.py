from .environment import *
from .apps import *
from .auth import *
from .celery import *
from .database import *
from .localization import *
from .logging import *
from .middleware import *
from .openweathermap import *
from .paths import *
from .restframework import *
from .swagger import *
from .templates import *


WSGI_APPLICATION = 'apps.wsgi.application'
ROOT_URLCONF = 'settings.urls'

ALLOWED_HOSTS = ['*']

STATIC_URL = '/dstatic/'
MEDIA_URL = '/dmedia/'
