import os

__all__ = ["DATABASES", ]

DB_DEFAULT_USER = os.getenv("TUVERMIND_DB_USER")
DB_DEFAULT_PASSWORD = os.getenv("TUVERMIND_DB_PASSWORD")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tuvermind',
        'USER': DB_DEFAULT_USER,
        'PASSWORD': DB_DEFAULT_PASSWORD,
        'HOST': 'tuvermind-db',
        'PORT': '5432',
    }
}
