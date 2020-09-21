from rest_framework import serializers

from api.bases.serializers import LoggedSerializerWrapper

from apps.todoes.models import TodoTaskHistory


class TodoTaskHistorySerializer(LoggedSerializerWrapper, serializers.ModelSerializer):
    class Meta:
        model = TodoTaskHistory
        fields = ['id', 'notify_at', 'completed']
