from django.db import transaction
from django.db.models import Q

from rest_framework import serializers

from api.bases.serializers import LoggedSerializerWrapper
from apps.todoes.models import TodoTask, TodoTaskReminder

__all__ = ["TodoTaskSerializer", ]


class RemindersSerializer(serializers.ModelSerializer):
    units = serializers.ChoiceField(choices=TodoTaskReminder.CHOICES)

    class Meta:
        model = TodoTaskReminder
        fields = ["id", "value", "units"]


class TodoTaskSerializer(LoggedSerializerWrapper, serializers.ModelSerializer):
    title = serializers.CharField(allow_blank=True)
    description = serializers.CharField(allow_blank=True)
    status = serializers.ChoiceField(
        choices=TodoTask.CHOICES,
        required=False,
        read_only=True
    )
    start_date = serializers.DateField(required=True, )
    start_time = serializers.TimeField(required=False)

    reminders = RemindersSerializer(many=True, required=False)

    class Meta:
        model = TodoTask

        fields = [
            "id", "title", "description", "start_date", "start_time",
            "duration", "status", "reminders", "created", "updated",
            "completed",
        ]

        read_only_fields = ["id", "created", "updated", "completed", "status"]

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
        instance.reminders.clear()

        if reminders:
            reminders_filter_query = Q()

            for reminder in reminders:
                TodoTaskReminder.objects.get_or_create(**reminder)
                reminders_filter_query |= Q(**reminder)

            instance.reminders.add(*TodoTaskReminder.objects.filter(
                reminders_filter_query
            ))

        instance.save()

        return instance
