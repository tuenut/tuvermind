from django.utils.timezone import now
from datetime import datetime as dt, timedelta as td

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from web.apps.openweathermap.models import OWMWeather, OWMData
from .serializers import OWMWeatherSerializer, OWMDataSerializer


class WeatherTypesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OWMWeather.objects.all()
    serializer_class = OWMWeatherSerializer


class WeatherHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OWMData.objects.all().order_by("-timestamp")
    serializer_class = OWMDataSerializer

    @action(url_path='(?P<date>[^/.]+)', detail=True)
    def date(self, request, *args, **kwargs):
        try:
            date = dt.strptime(kwargs.get("date"), "%d%m%Y")
        except ValueError:
            return Response("Please use as `/api/weather/history/date/DDMMYYYY/`.", status=status.HTTP_404_NOT_FOUND)

        queryset = self.get_queryset().filter(
            timestamp__day=date.day,
            timestamp__month=date.month,
            timestamp__year=date.year
        )
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    @action(detail=False)
    def current(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(timestamp__gte=now() - td(hours=3), timestamp__lt=now() + td(hours=3))
        pk_of_closest_object_to_now = min(map(lambda obj: (abs((now() - obj.timestamp).seconds), obj.pk), queryset))[1]
        instance = queryset.filter(pk=pk_of_closest_object_to_now)[0]

        serializer = self.get_serializer(instance)

        return Response(serializer.data)
