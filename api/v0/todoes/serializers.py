from django.db import transaction
from django.db.models import Q

from rest_framework import serializers

from api.bases.serializers import LoggedSerializerWrapper
from apps.todoes.models import TodoTask, ScheduledTodoTask, TodoTaskReminder

__all__ = ["TodoTaskSerializer", "ScheduledTodoTaskSerializer"]


class RemindersSerializer(serializers.ModelSerializer):
    dimension = serializers.ChoiceField(choices=TodoTaskReminder.DIMENSION_CHOICES)

    class Meta:
        model = TodoTaskReminder
        fields = ["value", "dimension"]


class TodoTaskSerializer(LoggedSerializerWrapper, serializers.ModelSerializer):
    reminders = RemindersSerializer(many=True)

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

    @staticmethod
    def _update_reminders(instance, reminders):
        for reminder in reminders:
            TodoTaskReminder.objects.get_or_create(**reminder)

        reminders_filter_query = Q()
        for reminder in reminders:
            reminders_filter_query |= Q(**reminder)

        instance.reminders.clear()
        instance.reminders.add(*TodoTaskReminder.objects.filter(reminders_filter_query))

        instance.save()

        return instance


class ScheduledTodoTaskSerializer(LoggedSerializerWrapper, serializers.ModelSerializer):
    class Meta:
        model = ScheduledTodoTask
        fields = [
            "id", "title", "description", "created", "updated", "history",
            "crontab_details", "clocked_details", "interval_details",
        ]
