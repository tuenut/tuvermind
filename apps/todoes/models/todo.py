import pprint

from django.db import models


class TodoTask(models.Model):
    title = models.CharField(max_length=32, null=False, default="")
    description = models.CharField(max_length=2048, null=False, default="")
    done = models.DateTimeField(null=True, default=None)

    created = models.DateTimeField(auto_now_add=True, null=False)
    updated = models.DateTimeField(auto_now=True, null=False)
    completed = models.DateTimeField(null=True)

    def __repr__(self):
        # for debug
        todo = {
            "title": self.title,
            "description": self.description
        }

        return f"<{self.__class__.__name__}>: {pprint.pformat(todo)}"


class ScheduledTodoTask(TodoTask):
    crontab_schedule = models.ForeignKey(
        "CrontabTODOSchedule",
        default=None, null=True, on_delete=models.SET_NULL
    )
    clocked_schedule = models.ForeignKey(
        "ClockedTODOSchedule",
        default=None, null=True, on_delete=models.SET_NULL
    )
    interval_schedule = models.ForeignKey(
        "IntervalTODOSchedule",
        default=None, null=True, on_delete=models.SET_NULL
    )


class TodoTaskReminder(models.Model):
    task = models.ForeignKey(
        "TodoTask",
        on_delete=models.CASCADE, related_name="reminders", related_query_name="reminder"
    )
    when = models.DateTimeField(null=True)
