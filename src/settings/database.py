import os

__all__ = ["DATABASES", ]

DB_USER = os.getenv("TUVERMIND_DB_USER")
DB_PASSWORD = os.getenv("TUVERMIND_DB_PASSWORD")
DB_HOST = os.getenv("TUVERMIND_DB_HOST")
DB_PORT = os.getenv("TUVERMIND_DB_PORT", 5432)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tuvermind',
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}
