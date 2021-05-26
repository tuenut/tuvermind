import pprint

from django.db import models


# from django_celery_beat.models import CrontabSchedule


class TodoTask(models.Model):
    """
    Notes
    -----
    - `reminder` can be used only if `start_date` is not null, or if cron schedule
     used (in future). Technically can be set up in db, but will ignored by
     celery notification tasks and UI.
    - default status on creation todo-task must be PENDING.
    """

    PENDING = "pending"  # must be set on create automatically
    IN_PROCESS = "inProcess"  # can be set by periodic task or by user
    COMPLETED = "completed"  # can be by user
    ARCHIVED = "archived"  # can be by user
    EXPIRED = "expired"  # must be set by periodic task
    SUSPENSE = "suspense"

    CHOICES = [
        (PENDING, PENDING),
        (IN_PROCESS, IN_PROCESS),
        (COMPLETED, COMPLETED),
        (ARCHIVED, ARCHIVED),
        (EXPIRED, EXPIRED),
        (SUSPENSE, SUSPENSE)
    ]

    DEFAULT = PENDING

    title = models.CharField(max_length=32, null=False, default="")
    description = models.CharField(max_length=2048, null=False, default="")

    start_date = models.DateTimeField(null=True, default=None)
    duration = models.IntegerField(null=True, default=None)

    created = models.DateTimeField(auto_now_add=True, null=False)
    updated = models.DateTimeField(auto_now=True, null=False)

    completed = models.DateTimeField(null=True)

    status = models.CharField(default=DEFAULT, choices=CHOICES, max_length=16)

    reminders = models.ManyToManyField("TodoTaskReminder")

    # TODO add cron-like schedule

    def __repr__(self):
        # for debug
        todo = {
            "id": self.id,
            "title": self.title,
            "description": self.description
        }

        return f"<{self.__class__.__name__}>: {pprint.pformat(todo)}"


class TodoTaskReminder(models.Model):
    MINUTES = "min"
    HOURS = "hour"
    DAYS = "day"
    WEEKS = "week"

    CHOICES = (
        (MINUTES, "Minutes"),
        (HOURS, "Hours"),
        (DAYS, "Days"),
        (WEEKS, "Weeks")
    )

    value = models.IntegerField(default=0)
    units = models.CharField(max_length=4, default=MINUTES, null=False)
