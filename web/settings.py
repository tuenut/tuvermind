import os
import logging

from web.config import *

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.56.102']
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_beat',

    'web',
    'web.apps',
    'web.apps.openweathermap',

]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'web.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
WSGI_APPLICATION = 'web.wsgi.application'
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.abspath('/var/www/tuvermind/static')  # os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.abspath('/var/www/tuvermind/media')  # os.path.join(BASE_DIR, 'media')

LOG_LEVEL = logging.DEBUG
LOG_DIR = os.path.join(BASE_DIR, '.logs')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)-8s >> [%(custom_call_trace)-36s] [%(process)d] [%(thread)d] %(message)s'
        },
        'task_formatter': {
            'format': '%(asctime)s %(levelname)-8s >> [%(custom_call_trace)-36s] [Task: %(task_id)s] %(message)s'
        },
        'basic_formatter': {
            'format': '%(asctime)s %(levelname)-8s >> [%(custom_call_trace)-36s] %(message)s'
        },
        'slack_formatter': {
            'format': '%(message)s'
        },
    },
    'filters': {},
    'loggers': {},
    'handlers': {
        'basic_stream': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'basic_formatter',
            "stream": "ext://sys.stdout"
        },
        'basic_file': {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'basic_formatter',
            'when': 'W6',
            'interval': 1,
            'backupCount': 10,
            'filename': 'default.log'
        },
    }
}
