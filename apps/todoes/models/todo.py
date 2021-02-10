import pprint

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class TodoTaskBase(models.Model):
    title = models.CharField(max_length=32, null=False, default="")
    description = models.CharField(max_length=2048, null=False, default="")

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


class TodoTask(TodoTaskBase):
    reminders = models.ManyToManyField("TodoTaskReminder")
    planned_completion_date = models.DateField(null=True, default=None)
    planned_completion_time = models.TimeField(null=True, default=None)


class ScheduledTodoTask(TodoTaskBase):
    repeats = models.ManyToManyField("RepeatVariant")


class RepeatVariant(models.Model):
    """
    Attributes
    ----------
    value: str
        may be a number for types of [IN_MINUTES, IN_DAY_OF_MONTH,
         IN_DAY_OF_WEEK]
            - IN_DAY_OF_MONTH like as `datetime.day`, if using day number
             larger, than amount of days in month then use last day of
             month.
            - IN_DAY_OF_WEEK like as `datetime.isoweekday()`
            - IN_IN_DATE_EVERY_YEAR uses format `MM.DD`. For example
             `12.31`.

    Notes
    -----
    Task may repeat in:
     - every N minutes (in UI must exist interface for switch to hours
      and days)
     - every N day each month
     - every year in `month.day` (like birthdays)
     - in day(s) of week

    Reminders needs for notifications.
    """

    # TODO Не корректные варианты повторения. Невозможно назначить "повторять каждый день в 9:30"
    # Надо, пожалуй, вернуться к варианту с кроном-like и, возможно, наследованием(толькоабстрактным) от модели из celery.

    IN_MINUTES = 0
    IN_DAY_OF_MONTH = 1
    IN_DATE_EVERY_YEAR = 2
    IN_DAY_OF_WEEK = 4

    types = [
        (IN_MINUTES, "repeat every selected count of minutes"),
        (IN_DAY_OF_MONTH, "repeat in selected day of every month"),
        (IN_DATE_EVERY_YEAR, "repeat every year in selected day"),
        (IN_DAY_OF_WEEK, "repeat every selected day of week")
    ]

    type = models.IntegerField(choices=types)
    value = models.CharField(max_length=8, default=None, null=None)
    reminders = models.ManyToManyField("TodoTaskReminder")

    def clean(self):
        if self.type in [
            self.IN_MINUTES, self.IN_DAY_OF_MONTH, self.IN_DAY_OF_WEEK
        ]:
            try:
                value = int(self.value)
            except ValueError:
                raise ValidationError(_(
                    "Value must be convertible into integer."
                ))

            if self.type == self.IN_DAY_OF_MONTH:
                if not (0 < value <= 31):
                    raise ValidationError(_(
                        "Value must be in `0 < day <= 31`."
                    ))

            elif self.type == self.IN_DAY_OF_WEEK:
                if not (0 < value <= 7):
                    raise ValidationError(_(
                        "Value must be in `0 < day <= 7`."
                    ))

        elif self.type == self.IN_DATE_EVERY_YEAR:
            try:
                month, day = self.value.split(".")
            except ValueError:
                raise ValidationError(_("Value must be like as `MM.DD`."))

            try:
                month = int(month)
            except ValueError:
                raise ValidationError(_(
                    "Month must be convertible into integer."
                ))
            if not (0 < month <= 12):
                raise ValidationError(_(
                    "Month must be in `0 < month <= 12`."
                ))

            try:
                day = int(day)
            except ValueError:
                raise ValidationError(_(
                    "Day must be convertible into integer."
                ))
            if not (0 < day <= 31):
                raise ValidationError(_(
                    "Month must be in `0 < month <= 31`."
                ))


class TodoTaskReminder(models.Model):
    MINUTES = "min"
    HOURS = "hour"
    DAYS = "day"
    WEEKS = "week"

    DIMENSION_CHOICES = (
        (MINUTES, "Minutes"),
        (HOURS, "Hours"),
        (DAYS, "Days"),
        (WEEKS, "Weeks")
    )

    value = models.IntegerField(default=0)
    units = models.CharField(max_length=4, default=MINUTES, null=False)
