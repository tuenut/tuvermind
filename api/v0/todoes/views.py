from django.utils.timezone import now
from django.db.models import Q

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v0.todoes.serializers import TodoTaskSerializer
from apps.todoes.models import TodoTask, TodoTaskReminder
from libs.logging.logger2 import Logger

__all__ = ["TodoTaskViewSet"]


class TodoTaskViewSet(Logger, viewsets.ModelViewSet):
    """
    Api usage example:
        {
            "id": int,
            "title": string,
            "description": string,
            "created": DateTime,
            "updated": DateTime,
            "start_date": DateTime,
            "end_date": DateTime,
            "status": string,
            "completed": DateTime,
            "reminders": [
                {
                    "value": "1",
                    "units": "min"
                },
                {
                    "value": 123,
                    "units": "day"
                }
            ]
        }

    - Reminder value can be int or string convertible to int.
    - Reminder units can be one of "min", "hour", "day", "week"
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

        instance = TodoTask.objects.get(pk=pk)

        if instance.completed:
            return Response(self.messages["TASK_UPDATING_NOK"])

        return super().update(request, *args, **kwargs)

    @action(detail=True)
    def complete(self, *args, pk=None, **kwargs):
        """This is only way to complete task."""
        instance = TodoTask.objects.get(pk=pk)

        if instance.completed:
            data = self.get_serializer(instance).data
            data.update(self.messages["TASK_COMPLETION_NOK"])

            return Response(data)
        else:
            instance.completed = now()
            instance.status = TodoTask.COMPLETED
            instance.save()

            data = self.get_serializer(instance).data
            data.update(self.messages["TASK_COMPLETION_OK"])

            return Response(data)

    @action(detail=False)
    def today(self, *args, **kwargs):
        """Shortcut to get tasks list filtered by today date."""

        today_or_none = Q(start_date=now()) | Q(start_date=None)
        today_todoes = self.get_queryset().filter(today_or_none, completed=None)

        page = self.paginate_queryset(today_todoes)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(today_todoes, many=True)
        return Response(serializer.data)

