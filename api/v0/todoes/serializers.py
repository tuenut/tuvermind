from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from api.bases.serializers import LoggedSerializerWrapper, DatetimeListField
from apps.todoes.models import TodoTaskBase, ScheduledTodoTask, TodoTaskReminder

__all__ = ["TodoTaskSerializer", "ScheduledTodoTaskSerializer"]


class TodoTaskSerializer(LoggedSerializerWrapper, serializers.ModelSerializer):
    class RemindersField(serializers.SlugRelatedField):
        def to_internal_value(self, data):
            try:
                return self.get_queryset().get(**{self.slug_field: data})
            except ObjectDoesNotExist:
                return serializers.DateTimeField().run_validation(data)
            except (TypeError, ValueError):
                self.fail('invalid')

    reminders = RemindersField(many=True, queryset=TodoTaskReminder.objects.all(), slug_field='when')

    class Meta:
        model = TodoTaskBase
        fields = ["id", "title", "description", "created", "updated", "completed", "reminders"]
        read_only_fields = ["created", "updated", "completed"]

    @transaction.atomic
    def save(self, **kwargs):
        self.is_valid(raise_exception=True)

        reminders = self.validated_data.pop("reminders", [])
        instance = super().save(**kwargs)

        reminders_set = set(
            obj.when if isinstance(obj, TodoTaskReminder) else obj
            for obj in reminders
        )

        existed = TodoTaskReminder.objects.filter(task=instance).values_list("when", flat=True)
        existed_set = set(DatetimeListField().to_representation(existed))

        to_create = reminders_set - existed_set
        to_remove = existed_set - reminders_set

        TodoTaskReminder.objects.filter(task=instance, when__in=to_remove).delete()
        TodoTaskReminder.objects.bulk_create([
            TodoTaskReminder(task=instance, when=reminder)
            for reminder in to_create
        ])

        return instance


class ScheduledTodoTaskSerializer(LoggedSerializerWrapper, serializers.ModelSerializer):
    class Meta:
        model = ScheduledTodoTask
        fields = [
            "id", "title", "description", "created", "updated", "history",
            "crontab_details", "clocked_details", "interval_details",
        ]
