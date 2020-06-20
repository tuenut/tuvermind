import os

__all__ = ["BASE_DIR", "STATIC_ROOT", "MEDIA_ROOT", "LOG_DIR", "SPA_BUILD_DIR", "STATICFILES_DIRS"]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, '.logs')

STATIC_ROOT = os.path.abspath('/var/www/tuvermind/static')  # os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.abspath('/var/www/tuvermind/media')  # os.path.join(BASE_DIR, 'media')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'public')
]

SPA_BUILD_DIR = os.path.join(BASE_DIR, 'spa')
if os.path.exists(SPA_BUILD_DIR):
    STATICFILES_DIRS.append(SPA_BUILD_DIR)
