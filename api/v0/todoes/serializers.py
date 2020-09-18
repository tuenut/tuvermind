from rest_framework import serializers

from .timeintervals.serializers import IntervalSerializer, ClockedSerializer, CrontabSerializer
from apps.todoes.models import TODO, RepeatableTODO, RepeatableTODOHistory, CrontabTODOSchedule

__all__ = ["TODOSerializer", ]


class TODOSerializer(serializers.HyperlinkedModelSerializer):
    schedule = serializers.PrimaryKeyRelatedField(
        source="repeatabletodo.crontab_schedule", allow_null=True, queryset=CrontabTODOSchedule.objects.filter(_todo=True)
    )


    class Meta:
        model = TODO
        fields = [
            "id", "title", "description", "created", "updated", "schedule",
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
