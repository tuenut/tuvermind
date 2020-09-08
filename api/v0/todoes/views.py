from rest_framework import viewsets, permissions

from .serializers import TODOSerializer
from apps.todoes.models import TODO


class TodoesViewSet(viewsets.ModelViewSet):
    queryset = TODO.objects.all()
    serializer_class = TODOSerializer
    permission_classes = [permissions.AllowAny]

    filterset_fields = {
        "repeatabletodo": ["isnull"]
    }

    ordering = ["created"]
    ordering_fields = []
