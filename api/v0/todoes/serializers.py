from django.db import transaction
from django.db.models import Q

from rest_framework import serializers

from api.bases.serializers import LoggedSerializerWrapper
from apps.todoes.models import TodoTask, ScheduledTodoTask, TodoTaskReminder, RepeatVariant

__all__ = ["TodoTaskSerializer", "ScheduledTodoTaskSerializer"]


class RemindersSerializer(serializers.ModelSerializer):
    units = serializers.ChoiceField(choices=TodoTaskReminder.DIMENSION_CHOICES)

    class Meta:
        model = TodoTaskReminder
        fields = ["value", "units"]


class RepeatsSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(RepeatVariant.types)
    reminders = RemindersSerializer(many=True)

    class Meta:
        model = RepeatVariant
        fields = ["type", "value", "reminders"]


class TodoTaskBaseSerializer(LoggedSerializerWrapper, serializers.ModelSerializer):
    title = serializers.CharField(allow_blank=True)
    description = serializers.CharField(allow_blank=True)


class TodoTaskSerializer(TodoTaskBaseSerializer):
    reminders = RemindersSerializer(many=True)

    class Meta:
        model = TodoTask
        fields = [
            "id", "title", "description", "created", "updated",
            "planned_completion_date", "planned_completion_time",
            "completed", "reminders"
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


class ScheduledTodoTaskSerializer(TodoTaskBaseSerializer):
    title = serializers.CharField(allow_blank=True)
    description = serializers.CharField(allow_blank=True)
    repeats = RepeatsSerializer(many=True)

    class Meta:
        model = ScheduledTodoTask
        fields = [
            "id", "title", "description", "created", "updated",
            "completed", "repeats",
        ]
        read_only_fields = ["created", "updated", "completed"]

    @transaction.atomic
    def create(self, validated_data):
        repeats = validated_data.pop("repeats", [])
        instance = super().create(validated_data)
        instance = self._update_repeats(instance, repeats)

        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        repeats = validated_data.pop("repeats", [])
        instance = self._update_repeats(instance, repeats)

        return super().update(instance, validated_data)

    def _update_repeats(self, instance, repeats):
        instance.repeats.clear()

        if repeats:
            repeats_filter_query = Q()

            for repeat_object in repeats:
                reminder = ...

        return instance
