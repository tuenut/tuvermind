from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from api.bases.serializers import LoggedSerializerWrapper, IntegerListField
from apps.todoes.models import TodoTask, ScheduledTodoTask, TodoTaskReminder

__all__ = ["TodoTaskSerializer", "ScheduledTodoTaskSerializer"]


class RemindersSerializer(serializers.SlugRelatedField, serializers.IntegerField):
    def to_internal_value(self, data):
        data = super(serializers.SlugRelatedField, self).to_internal_value(data)

        try:
            return self.get_queryset().get(**{self.slug_field: data})
        except ObjectDoesNotExist:
            return serializers.IntegerField().run_validation(data)
        except (TypeError, ValueError):
            self.fail('invalid')


class TodoTaskSerializer(LoggedSerializerWrapper, serializers.ModelSerializer):
    reminders = RemindersSerializer(many=True, queryset=TodoTaskReminder.objects.all(), slug_field='remind_for_minutes')

    class Meta:
        model = TodoTask
        fields = [
            "id", "title", "description", "created", "updated", "planned_completion_date",
            "planned_completion_time", "completed", "reminders"
        ]
        read_only_fields = ["created", "updated", "completed"]

    @transaction.atomic
    def create(self, validated_data):
        reminders = validated_data.pop("reminders", [])
        instance = super().create(validated_data)
        instance = self._update_reminders(instance, reminders)

        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        reminders = validated_data.pop("reminders", [])
        instance = self._update_reminders(instance, reminders)

        return super().update(instance, validated_data)

    def _update_reminders(self, instance, reminders):
        reminders_set = set(
            value.remind_for_minutes if isinstance(value, TodoTaskReminder) else int(value)
            for value in reminders
        )
        existed_set = set(instance.reminders.values_list("remind_for_minutes", flat=True))

        values_to_create = reminders_set - existed_set
        values_to_remove = existed_set - reminders_set

        instance.reminders.filter(remind_for_minutes__in=values_to_remove).delete()
        instance.reminders.add(*[
            TodoTaskReminder.objects.get_or_create(remind_for_minutes=value)[0]
            for value in values_to_create
        ])

        instance.save()

        return instance


class ScheduledTodoTaskSerializer(LoggedSerializerWrapper, serializers.ModelSerializer):
    class Meta:
        model = ScheduledTodoTask
        fields = [
            "id", "title", "description", "created", "updated", "history",
            "crontab_details", "clocked_details", "interval_details",
        ]
