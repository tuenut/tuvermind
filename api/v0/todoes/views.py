from django.utils.timezone import now
from django.db.models import Q
from django.utils.decorators import method_decorator

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v0.todoes.serializers import TodoTaskSerializer
from apps.todoes.models import TodoTask, TodoTaskReminder
from libs.logging.logger2 import Logger

from drf_yasg.utils import swagger_auto_schema
from drf_yasg.inspectors import SwaggerAutoSchema

__all__ = ["TodoTaskViewSet"]


class ExcludesAnyParametersExceptPagintaionSwaggerAutoSchema(SwaggerAutoSchema):
    def get_query_parameters(self):
        return self.get_pagination_parameters()


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(operation_summary="Get list of todoes.")
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_summary="Create new todo.",
        operation_description="""\
You can set title, description, dates of start and end task, also set of \
reminders. Other parameters will set automatically.
For change status - use special actions."""
    )
)
class TodoTaskViewSet(Logger, viewsets.ModelViewSet):
    """That view represents TODOes.

    TODOes are tasks that you would like to complete later.
    You can set a planned start date for the task, reminders before starting.

    """
    # TODO: remove notes below and remove support that from code
    # - Reminder value can be int or string convertible to int.
    # - Reminder units can be one of "min", "hour", "day", "week"

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

    def update(self, request, *args, pk=None, **kwargs):
        """Edit task.

        You can not change a completed task.
        """

        instance = TodoTask.objects.get(pk=pk)

        if instance.completed:
            return Response(self.messages["TASK_UPDATING_NOK"])

        return super().update(request, *args, **kwargs)

    @action(detail=True)
    def complete(self, *args, pk=None, **kwargs):
        """This is the only way to complete task."""

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

    @swagger_auto_schema(auto_schema=ExcludesAnyParametersExceptPagintaionSwaggerAutoSchema)
    @action(detail=False)
    def today(self, *args, **kwargs):
        """Shortcut to get tasks list filtered by today date."""

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
