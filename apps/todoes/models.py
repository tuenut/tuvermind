import pprint

from django.db import models

__all__ = ["TODO", "RepeatableTODO", "RepeatableTODOHistory"]


class TODO(models.Model):
    title = models.CharField(max_length=32, null=False, default="")
    description = models.CharField(max_length=2048, null=False, default="")
    done = models.DateTimeField(null=True, default=None)

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
    repeat_every_minutes = models.IntegerField(null=False, default=0)
    start_at = models.DateTimeField(null=False, auto_now_add=True)
    history = models.ManyToManyField("RepeatableTODOHistory")


class RepeatableTODOHistory(models.Model):
    notify_at = models.DateTimeField(null=True)
    completion_confirmation = models.BooleanField(null=False, default=False)
