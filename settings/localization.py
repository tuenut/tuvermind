from django.utils.translation import gettext_lazy as _

__all__ = ["LANGUAGE_CODE", "TIME_ZONE", "USE_TZ", "USE_L10N", "USE_I18N"]


LANGUAGES = [
    ('ru', _('Russian')),
    ('en', _('English')),
]

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
