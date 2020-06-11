from __future__ import absolute_import, unicode_literals

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from apps.celery import app as celery_app
import settings

__all__ = ('celery_app', 'settings')
