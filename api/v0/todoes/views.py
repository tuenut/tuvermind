from django.utils.timezone import now
from django.db import transaction

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v0.todoes.serializers import TodoTaskSerializer, ScheduledTodoTaskSerializer
from apps.todoes.models import TodoTask, TodoTaskReminder, ScheduledTodoTask
from libs.logging.logger2 import Logger

__all__ = ["TodoTaskViewSet", "ScheduledTodoTaskViewSet"]


class TodoTaskViewSet(Logger, viewsets.ModelViewSet):
    queryset = TodoTask.objects.all()
    serializer_class = TodoTaskSerializer
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

    def update(self, request, *args, pk=None, **kwargs):
        try:
            instance = TodoTask.objects.get(pk=pk)
        except TodoTask.DoesNotExist:
            raise

        if instance.completed:
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

        if instance.completed:
            data = self.get_serializer(request).data
            data.update(self.COMPLETE_TASK_NOK)

            return Response(data)
        else:
            instance.completed = now()
            instance.save()

            data = self.get_serializer(request).data
            data.update(self.COMPLETE_TASK_OK)

            return Response(data)


class ScheduledTodoTaskViewSet(Logger, viewsets.ModelViewSet):
    queryset = ScheduledTodoTask.objects.all()
    serializer_class = ScheduledTodoTaskSerializer
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
            instance = ScheduledTodoTask.objects.get(pk=kwargs['pk'])
        except ScheduledTodoTask.DoesNotExist:
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
    def complete_task(self, request, pk=None):
        try:
            instance = ScheduledTodoTask.objects.get(pk=pk)
        except ScheduledTodoTask.DoesNotExist:
            raise

        history = instance.todotaskhistory_set.first()  # type: TodoTaskReminder

        if history:
            if not history.completed:
                history.completed = now()
                history.save()
            else:
                data = self.get_serializer(request).data
                data.update(self.COMPLETE_TASK_NOK)

                return Response(data)
        else:
            TodoTaskReminder.objects.create(task=instance, completed=now())

        data = self.get_serializer(request).data
        data.update(self.COMPLETE_TASK_OK)

        return Response(data)
