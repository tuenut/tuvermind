from django.db import models
from django_celery_beat.models import CrontabSchedule, ClockedSchedule, IntervalSchedule


class CrontabTODOSchedule(CrontabSchedule):
    # TODO заменить на пользователя в дальнейшем.
    _todo = models.BooleanField(default=True)


class ClockedTODOSchedule(ClockedSchedule):
    # TODO заменить на пользователя в дальнейшем.
    _todo = models.BooleanField(default=True)


class IntervalTODOSchedule(IntervalSchedule):
    # TODO заменить на пользователя в дальнейшем.
    _todo = models.BooleanField(default=True)
