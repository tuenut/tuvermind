__all__ = ["INSTALLED_APPS", ]

INSTALLED_APPS = [
    'corsheaders',
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
    'apps.todoes'
]
