import os

from django.utils.translation import gettext_lazy as _

__all__ = [
    "INSTALLED_APPS", "BASE_DIR", "LOG_DIR", "LANGUAGES", "LANGUAGE_CODE",
    "STATICFILES_DIRS", "USE_TZ", "USE_I18N", "USE_L10N", "TIME_ZONE",
    "MEDIA_ROOT", "STATIC_ROOT", "ROOT_URLCONF", "MEDIA_URL", "STATIC_URL",
    "WSGI_APPLICATION", "AUTH_PASSWORD_VALIDATORS", "TEMPLATES", "MIDDLEWARE",
]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

WSGI_APPLICATION = 'apps.wsgi.application'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_beat',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',

    'apps.openweathermap',
    'apps.todoes',
    'drf_yasg',
    'debug_toolbar',

    "django_extensions"
]

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ]
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

LOG_DIR = os.path.join(BASE_DIR, '.logs')
STATIC_ROOT = os.path.abspath('/var/www/tuvermind/static')
MEDIA_ROOT = os.path.abspath('/var/www/tuvermind/media')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'public')
]

ROOT_URLCONF = 'settings.urls'

STATIC_URL = '/dstatic/'
MEDIA_URL = '/dmedia/'

LANGUAGES = [
    ('ru', _('Russian')),
    ('en', _('English')),
]
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
