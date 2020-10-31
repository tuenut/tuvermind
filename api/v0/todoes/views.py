from django.utils.timezone import now
from django.db.models import Q

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v0.todoes.serializers import TodoTaskSerializer, ScheduledTodoTaskSerializer
from apps.todoes.models import TodoTask, TodoTaskReminder, ScheduledTodoTask
from libs.logging.logger2 import Logger

__all__ = ["TodoTaskViewSet", "ScheduledTodoTaskViewSet"]


class TodoTaskViewSet(Logger, viewsets.ModelViewSet):
    """
    Api usage example:
        {
            "id": 3,
            "title": "string",
            "description": "string",
            "created": "2020-10-31T16:18:14.729107Z",
            "updated": "2020-10-31T20:19:32.242457Z",
            "planned_completion_date": null,
            "planned_completion_time": null,
            "completed": null,
            "reminders": [
                {
                    "value": "1",
                    "dimension": "min"
                },
                {
                    "value": 123,
                    "dimension": "day"
                }
            ]
        }

    - Reminder value can be int or string convertible to int.
    - Reminder dimension can be one of "min", "hour", "day", "week"
    """

    queryset = TodoTask.objects.all()
    serializer_class = TodoTaskSerializer
    permission_classes = [permissions.AllowAny]

    filterset_fields = {}

    ordering = ["created"]
    ordering_fields = []

    messages = {
        "TASK_UPDATING_NOK": {
            "_operation_result": {
                "message": "Cant update completed task.",
                "code": "NOK"
            }
        },
        "TASK_COMPLETION_OK": {
            "_operation_result": {
                "message": "Task complete.",
                "code": "OK"
            }
        },
        "TASK_COMPLETION_NOK": {
            "_operation_result": {
                "message": "Task already completed.",
                "code": "NOK"
            }
        }
    }

    def update(self, request, *args, pk=None, **kwargs):
        """Prevent update already completed task."""

        try:
            instance = TodoTask.objects.get(pk=pk)
        except TodoTask.DoesNotExist:
            raise

        if instance.completed:
            return Response(self.messages["TASK_UPDATING_NOK"])

        return super().update(request, *args, **kwargs)

    @action(detail=True)
    def complete(self, *args, pk=None, **kwargs):
        """This is only way to complete task."""
        try:
            instance = TodoTask.objects.get(pk=pk)
        except TodoTask.DoesNotExist:
            raise

        if instance.completed:
            data = self.get_serializer(instance).data
            data.update(self.messages["TASK_COMPLETION_NOK"])

            return Response(data)
        else:
            instance.completed = now()
            instance.save()

            data = self.get_serializer(instance).data
            data.update(self.messages["TASK_COMPLETION_OK"])

            return Response(data)

    @action(detail=False)
    def today(self, *args, **kwargs):
        """Shortcut to get tasks list filtered by today date."""

        today_or_none = Q(planned_completion_date=now()) | Q(planned_completion_date=None)
        today_todoes = self.get_queryset().filter(today_or_none, completed=None)

        page = self.paginate_queryset(today_todoes)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(today_todoes, many=True)
        return Response(serializer.data)


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
