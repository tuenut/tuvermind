from .environment import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

__all__ = ["DATABASES", "DEFAULT_AUTO_FIELD"]

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
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
