from datetime import datetime as dt

from rest_framework import viewsets, filters

from web.apps.openweathermap.models import OWMWeather, OWMData
from .serializers import OWMWeatherSerializer, OWMDataSerializer


class WeatherTypesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OWMWeather.objects.all()
    serializer_class = OWMWeatherSerializer


class WeatherHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OWMData.objects.all().order_by("-timestamp")
    serializer_class = OWMDataSerializer

    class DateFilterBackend(filters.BaseFilterBackend):
        def filter_queryset(self, request, queryset, view):

            try:
                date = dt.strptime(request.query_params.get("date"), "%d%m%Y")
            except ValueError:
                return queryset
            else:
                return queryset.filter(
                    timestamp__day=date.day,
                    timestamp__month=date.month,
                    timestamp__year=date.year
                )

    filter_backends = [DateFilterBackend]
