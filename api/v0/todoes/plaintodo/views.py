from django.utils.timezone import now

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from libs.logging.logger2 import Logger

from api.v0.todoes.plaintodo.serializers import TODOSerializer
from apps.todoes.models import TodoTask, TodoTaskHistory


class TodoTaskViewSet(Logger, viewsets.ModelViewSet):
    queryset = TodoTask.objects.all()
    serializer_class = TODOSerializer
    permission_classes = [permissions.AllowAny]

    filterset_fields = {}

    ordering = ["created"]
    ordering_fields = []

    UPDATE_NOK = {
        "_operation_result": {
            "message": "Cant update completed task.",
            "code": "NOK"
        }
    }

    def update(self, request, *args, **kwargs):
        try:
            instance = TodoTask.objects.get(pk=kwargs['pk'])
        except TodoTask.DoesNotExist:
            raise

        history = instance.todotaskhistory_set.first()

        if history and history.completed:
            return Response(self.UPDATE_NOK)

        return super().update(request, *args, **kwargs)

    COMPLETE_TASK_OK = {
        "_operation_result": {
            "message": "Task complete.",
            "code": "OK"
        }
    }
    COMPLETE_TASK_NOK = {
        "_operation_result": {
            "message": "Task already completed.",
            "code": "NOK"
        }
    }

    @action(detail=True)
    def complete(self, request, pk=None):
        try:
            instance = TodoTask.objects.get(pk=pk)
        except TodoTask.DoesNotExist:
            raise

        history = instance.todotaskhistory_set.first()  # type: TodoTaskHistory

        if history:
            if not history.completed:
                history.completed = now()
                history.save()
            else:
                data = self.get_serializer(request).data
                data.update(self.COMPLETE_TASK_NOK)

                return Response(data)
        else:
            TodoTaskHistory.objects.create(task=instance, completed=now())

        data = self.get_serializer(request).data
        data.update(self.COMPLETE_TASK_OK)

        return Response(data)
