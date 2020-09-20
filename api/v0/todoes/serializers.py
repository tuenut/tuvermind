from rest_framework import serializers

from .timeintervals.serializers import IntervalSerializer, ClockedSerializer, CrontabSerializer
from apps.todoes.models import TodoProxy, TODO, RepeatableTODO, RepeatableTODOHistory, CrontabTODOSchedule, \
    ClockedTODOSchedule, IntervalTODOSchedule

__all__ = ["TODOSerializer", ]


class TODOSerializer(serializers.HyperlinkedModelSerializer):
    crontab_schedule = serializers.PrimaryKeyRelatedField(
        source="repeatabletodo.crontab_schedule",
        allow_null=True,
        queryset=CrontabTODOSchedule.objects.filter(_todo=True)
    )
    clocked_schedule = serializers.PrimaryKeyRelatedField(
        source="repeatabletodo.clocked_schedule",
        allow_null=True,
        queryset=ClockedTODOSchedule.objects.filter(_todo=True)
    )
    interval_schedule = serializers.PrimaryKeyRelatedField(
        source="repeatabletodo.interval_schedule",
        allow_null=True,
        queryset=IntervalTODOSchedule.objects.filter(_todo=True)
    )
    crontab = CrontabSerializer(source="repeatabletodo.crontab_schedule")

    class Meta:
        model = TodoProxy
        fields = [
            "id", "title", "description", "created", "updated", "crontab_schedule", "clocked_schedule",
            "interval_schedule", "crontab"
        ]

    def create(self, validated_data):
        repeatable = validated_data.pop("repeatabletodo", {})
        validated_data = {**validated_data, **repeatable}

        ModelClass = RepeatableTODO if repeatable else TODO
        todo = ModelClass.objects.create(**validated_data)

        return todo

    def update(self, instance, validated_data):
        repeatable = validated_data.pop("repeatabletodo", {})
        validated_data = {**validated_data, **repeatable}

        ModelClass = RepeatableTODO if repeatable else TODO

        # TODO надо все же пересмотреть структуру моделек с todo
        instance = ModelClass.objects.get()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance
