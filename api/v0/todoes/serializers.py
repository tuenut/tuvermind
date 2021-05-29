from django.db import transaction
from django.db.models import Q

from rest_framework import serializers

from api.bases.serializers import LoggedSerializerWrapper
from apps.todoes.models import TodoTask, TodoTaskReminder

__all__ = ["TodoTaskSerializer", ]


class RemindersSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoTaskReminder
        fields = ["id", "when"]


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

    def _update_reminders(self, instance, new_reminders):
        new_reminders_set = set(map(lambda r: r["when"], new_reminders))
        old_reminders_set = set(
            instance.reminders.values_list("when", flat=True))

        instance.reminders \
            .filter(when__in=old_reminders_set - new_reminders_set) \
            .delete()

        instance.reminders.add(*list(map(
            lambda when: TodoTaskReminder.objects.create(when=when),
            list(new_reminders_set - old_reminders_set)
        )))

        instance.save()

        return instance
