from rest_framework import serializers

from apps.todoes.models import ClockedTODOSchedule, CrontabTODOSchedule, IntervalTODOSchedule

__all__ = ["IntervalSerializer", ]


class IntervalSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntervalTODOSchedule
        fields = ["id", "every", "period"]


class ClockedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClockedTODOSchedule
        fields = ["id", "clocked_time", "enabled"]


class CrontabSerializer(serializers.ModelSerializer):
    timezone = serializers.CharField()

    class Meta:
        model = CrontabTODOSchedule
        fields = [
            "id", "minute", "hour", "day_of_week", "day_of_month", "month_of_year", "timezone"
        ]
