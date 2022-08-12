import os

__all__ = ["BASE_DIR", "STATICFILES_DIRS", "STATIC_ROOT", "MEDIA_ROOT"]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MEDIA_ROOT = os.path.abspath('/var/www/tuvermind/media')
STATIC_ROOT = os.path.abspath('/var/www/tuvermind/static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'public'),
]
