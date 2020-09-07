from django.db import models

# Create your models here.


class TODO(models.Model):
    title = models.CharField(max_length=32, null=False, default="")
    description = models.CharField(max_length=2048, null=False, default="")
    repeatable = models.BooleanField(null=False, default=False)


class RepeatableTODO(TODO):
    repeat_every_minutes = models.IntegerField(null=False, default=0)
    start_at = models.DateTimeField(null=False, auto_now_add=True)
    history = models.ManyToManyField("RepeatableTODOHistory")


class RepeatableTODOHistory(models.Model):
    notify_at = models.DateTimeField(null=True)
    completion_confirmation = models.BooleanField(null=False, default=False)
