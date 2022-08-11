from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

__all__ = ['app', ]

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

app = Celery('tuvermind', backend='redis')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
