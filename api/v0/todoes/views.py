from django.utils.timezone import now
from django.db.models import Q
from django.utils.decorators import method_decorator

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from libs.logging.logger2 import Logger

from apps.todoes.models import TodoTask

from api.v0.todoes.serializers import TodoTaskSerializer
from api.v0.todoes.swaggerdocs import (
    todoes_list_docs, todoes_create_docs, todoes_partial_update_docs,
    todoes_destroy_docs, todoes_retrieve_docs, todoes_update_docs,
    todoes_complete_docs, todoes_today_docs
)

__all__ = ["TodoTaskViewSet"]


@method_decorator(name="list", decorator=todoes_list_docs)
@method_decorator(name="create", decorator=todoes_create_docs)
@method_decorator(name="destroy", decorator=todoes_destroy_docs)
@method_decorator(name="retrieve", decorator=todoes_retrieve_docs)
@method_decorator(name="partial_update", decorator=todoes_partial_update_docs)
class TodoTaskViewSet(Logger, viewsets.ModelViewSet):
    """That view represents TODOes.

    TODOes are tasks that you would like to complete later.
    You can set a planned start date for the task, reminders before starting.

    """
    # TODO: remove notes below and remove support that from code
    # - Reminder value can be int or string convertible to int.
    # - Reminder units can be one of "min", "hour", "day", "week"
    # TODO add `archive` action

    queryset = TodoTask.objects.all()
    serializer_class = TodoTaskSerializer
    permission_classes = [permissions.AllowAny]

    filterset_fields = {
        "created": ["exact", "lte", "gte"],
        "updated": ["exact", "lte", "gte"],
        "start_date": ["exact", "lte", "gte"],
        "title": ["exact", "contains"]
    }

    ordering = ["created"]
    ordering_fields = ["created", "updated", "start_date"]

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

    @todoes_update_docs
    def update(self, request, *args, pk=None, **kwargs):
        instance = TodoTask.objects.get(pk=pk)

        if instance.completed:
            return Response(self.messages["TASK_UPDATING_NOK"])

        return super().update(request, *args, **kwargs)

    @todoes_complete_docs
    @action(detail=True)
    def complete(self, request, *args, pk=None, **kwargs):
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

    @todoes_today_docs
    @action(detail=False)
    def today(self, request, *args, **kwargs):
        today_todoes = self.get_queryset() \
            .filter(Q(start_date=now()) | Q(start_date=None), completed=None)

        page = self.paginate_queryset(today_todoes)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(today_todoes, many=True)
            response = Response(serializer.data, status=status.HTTP_200_OK)

        return response
