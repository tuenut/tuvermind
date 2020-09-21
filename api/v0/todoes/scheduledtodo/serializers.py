from rest_framework import serializers

from api.bases.serializers import LoggedSerializerWrapper
from api.v0.todoes.timeintervals.serializers import CrontabSerializer, ClockedSerializer, IntervalSerializer
from apps.todoes.models import ScheduledTodoTask


class TODOSerializer(LoggedSerializerWrapper, serializers.HyperlinkedModelSerializer):
    crontab_schedule = CrontabSerializer(source="repeatabletodo.crontab_schedule", required=False, allow_null=True)
    clocked_schedule = ClockedSerializer(source="repeatabletodo.clocked_schedule", required=False, allow_null=True)
    interval_schedule = IntervalSerializer(
        source="repeatabletodo.interval_schedule", required=False, allow_null=True
    )

    class Meta:
        model = ScheduledTodoTask
        fields = [
            "id", "title", "description", "created", "updated", "crontab_schedule", "clocked_schedule",
            "interval_schedule"
        ]

    # def create(self, validated_data):
    #     repeatable = validated_data.pop("repeatabletodo", {})
    #     validated_data = {**validated_data, **repeatable}
    #
    #     todo = RepeatableTODO.objects.create(**validated_data)
    #
    #     return todo

    # def update(self, instance, validated_data):
    #     repeatable = validated_data.pop("repeatabletodo", {})
    #     validated_data = {**validated_data, **repeatable}
    #
    #     instance = RepeatableTODO.objects.get()
    #
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #
    #     instance.save()
    #
    #     return instance