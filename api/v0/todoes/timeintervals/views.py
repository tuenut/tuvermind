from rest_framework import viewsets, permissions

from .serializers import IntervalSerializer, CrontabSerializer, ClockedSerializer
from apps.todoes.models import CrontabTODOSchedule, ClockedTODOSchedule, IntervalTODOSchedule

__all__ = ["IntervalsViewSet", "CrontabViewsSet", "ClockedViewsSet"]


class IntervalsViewSet(viewsets.ModelViewSet):
    # TODO фильтровать по пользователям, когда прикручу
    queryset = IntervalTODOSchedule.objects.filter(_todo=True)
    serializer_class = IntervalSerializer
    permission_classes = [permissions.AllowAny]

    filterset_fields = {
        "id": ["exact"],
        "minute": ["exact"],
        "hour": ["exact"],
        "day_of_week": ["exact"],
        "day_of_month": ["exact"],
        "month_of_year": ["exact"],
        "timezone": ["exact", "contains"]
    }


class CrontabViewsSet(viewsets.ModelViewSet):
    queryset = CrontabTODOSchedule.objects.filter(_todo=True)
    serializer_class = CrontabSerializer
    permission_classes = [permissions.AllowAny]


class ClockedViewsSet(viewsets.ModelViewSet):
    queryset = ClockedTODOSchedule.objects.filter(_todo=True)
    serializer_class = ClockedSerializer
    permission_classes = [permissions.AllowAny]
