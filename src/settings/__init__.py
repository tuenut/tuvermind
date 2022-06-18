import os

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
DEBUG = bool(os.getenv("TUVERMIND_DEBUG"))
SECRET_KEY = os.getenv("TUVERMIND_SECRET_KEY", None)

STATIC_URL = '/dstatic/'
MEDIA_URL = '/dmedia/'
