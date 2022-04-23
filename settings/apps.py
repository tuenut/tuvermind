__all__ = ["INSTALLED_APPS", ]

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
