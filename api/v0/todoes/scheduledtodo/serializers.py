from rest_framework import serializers

from api.bases.serializers import LoggedSerializerWrapper
from api.v0.todoes.history.serializers import TodoTaskHistorySerializer
from api.v0.todoes.timeintervals.serializers import CrontabSerializer, ClockedSerializer, IntervalSerializer

from apps.todoes.models import ScheduledTodoTask


class ScheduledTodoTaskSerializer(LoggedSerializerWrapper, serializers.ModelSerializer):
    history = TodoTaskHistorySerializer(source="todotaskhistory_set", read_only=True, many=True)
    crontab_details = CrontabSerializer(source="crontab_schedule", read_only=True)
    clocked_details = ClockedSerializer(source="clocked_schedule", read_only=True)
    interval_details = IntervalSerializer(source="interval_schedule", read_only=True)

    class Meta:
        model = ScheduledTodoTask
        fields = [
            "id", "title", "description", "created", "updated", "history",
            "crontab_details", "clocked_details", "interval_details",
            "crontab_schedule", "clocked_schedule", "interval_schedule"
        ]
