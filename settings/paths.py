import os

__all__ = ["BASE_DIR", "STATIC_ROOT", "MEDIA_ROOT", "LOG_DIR"]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.abspath('/var/www/tuvermind/static')  # os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.abspath('/var/www/tuvermind/media')  # os.path.join(BASE_DIR, 'media')
LOG_DIR = os.path.join(BASE_DIR, '.logs')
