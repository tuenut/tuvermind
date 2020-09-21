from rest_framework import viewsets, permissions

from api.v0.todoes.plaintodo.serializers import TODOSerializer
from apps.todoes.models import TodoTask


class TodoTaskViewSet(viewsets.ModelViewSet):
    queryset = TodoTask.objects.all()
    serializer_class = TODOSerializer
    permission_classes = [permissions.AllowAny]

    filterset_fields = {

    }

    ordering = ["created"]
    ordering_fields = []