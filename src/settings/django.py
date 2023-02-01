import os

from django.utils.translation import gettext_lazy as _


__all__ = [
    "LANGUAGES",
    "LANGUAGE_CODE",
    "TIME_ZONE",
    "USE_TZ",
    "USE_I18N",
    "USE_L10N",
    "BASE_DIR",
    "STATICFILES_DIRS",
    "STATIC_ROOT",
    "MEDIA_ROOT",
    "TEMPLATES",
    "MIDDLEWARE",
    "INSTALLED_APPS",
    "AUTH_PASSWORD_VALIDATORS",
    "STATIC_URL",
    "MEDIA_URL",
    "ROOT_URLCONF",
    "ALLOWED_HOSTS",
    "WSGI_APPLICATION",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_celery_beat",
    "rest_framework",
    "rest_framework.authtoken",
    "django_filters",
    "apps.openweathermap",
    "drf_yasg",
]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MEDIA_ROOT = os.path.abspath("/tmp/tuvermind/media")
STATIC_ROOT = os.path.abspath("/tmp/tuvermind/static")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "public"),
]

WSGI_APPLICATION = 'apps.wsgi.application'
ROOT_URLCONF = 'settings.urls'

ALLOWED_HOSTS = ['*']

STATIC_URL = '/dstatic/'
MEDIA_URL = '/dmedia/'

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "libs.middlewares.log_request_id.LogRequestIdMiddleware",
]

LANGUAGES = [
    ("ru", _("Russian")),
    ("en", _("English")),
]
LANGUAGE_CODE = "ru"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
