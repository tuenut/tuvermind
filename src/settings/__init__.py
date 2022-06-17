import os

from .celery import *
from .database import *
from .django import *
from .logging import *
from .restframework import *
from .swagger import *
from .openweathermap import *

ALLOWED_HOSTS = ['*']

SECRET_KEY = os.getenv("TUVERMIND_SECRET_KEY")
