from rest_framework import serializers

from api.bases.serializers import LoggedSerializerWrapper
from api.v0.todoes.history.serializers import TodoTaskHistorySerializer

from apps.todoes.models import TodoTask


class TODOSerializer(LoggedSerializerWrapper, serializers.ModelSerializer):
    history = TodoTaskHistorySerializer(source="todotaskhistory_set", read_only=True, many=True)

    class Meta:
        model = TodoTask
        fields = ["id", "title", "description", "created", "updated", "history"]
