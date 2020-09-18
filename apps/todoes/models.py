import pprint

from django.db import models
from django_celery_beat.models import CrontabSchedule, ClockedSchedule, IntervalSchedule

__all__ = [
    "TODO", "RepeatableTODO", "RepeatableTODOHistory", "CrontabTODOSchedule", "ClockedTODOSchedule",
    "IntervalTODOSchedule"
]


class CrontabTODOSchedule(CrontabSchedule):
    # TODO заменить на пользователя в дальнейшем.
    _todo = models.BooleanField(default=True)


class ClockedTODOSchedule(ClockedSchedule):
    # TODO заменить на пользователя в дальнейшем.
    _todo = models.BooleanField(default=True)


class IntervalTODOSchedule(IntervalSchedule):
    # TODO заменить на пользователя в дальнейшем.
    _todo = models.BooleanField(default=True)


class TODO(models.Model):
    title = models.CharField(max_length=32, null=False, default="")
    description = models.CharField(max_length=2048, null=False, default="")
    done = models.DateTimeField(null=True, default=None)

    until = models.ForeignKey("ClockedTODOSchedule", default=None, null=True, on_delete=models.SET_NULL)

    created = models.DateTimeField(auto_now_add=True, null=False)
    updated = models.DateTimeField(auto_now=True, null=False)

    def __repr__(self):
        # for debug
        todo = {
            "title": self.title,
            "description": self.description
        }

        try:
            repeatable = {
                "repeat_every_minutes": self.repeatabletodo.repeat_every_minutes,
                "start_at": self.repeatabletodo.start_at
            }
        except TODO.DoesNotExist:
            repeatable = {}

        todo["repeatable"] = repeatable

        return pprint.pformat(todo)


class RepeatableTODO(TODO):
    # TODO попробовать связать с celery_beat intervals
    crontab_schedule = models.ForeignKey("CrontabTODOSchedule", default=None, null=True, on_delete=models.SET_NULL)
    interval_schedule = models.ForeignKey("IntervalTODOSchedule", default=None, null=True, on_delete=models.SET_NULL)
    history = models.ManyToManyField("RepeatableTODOHistory")


class RepeatableTODOHistory(models.Model):
    notify_at = models.DateTimeField(null=True)
    completion_confirmation = models.BooleanField(null=False, default=False)
