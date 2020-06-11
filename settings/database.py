from settings.secret import DB_DEFAULT_USER, DB_DEFAULT_PASSWORD

__all__ = ["DATABASES", ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tuvermind',
        'USER': DB_DEFAULT_USER,
        'PASSWORD': DB_DEFAULT_PASSWORD,
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
