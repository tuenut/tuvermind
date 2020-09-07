from rest_framework import viewsets

from apps.openweathermap.models import OWMWeather, OWMData
from .serializers import OWMWeatherSerializer, OWMDataSerializer


class WeatherTypesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OWMWeather.objects.all()
    serializer_class = OWMWeatherSerializer


class WeatherViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OWMData.objects.all().order_by("-timestamp")

    serializer_class = OWMDataSerializer

    filterset_fields = {
        "timestamp": ["exact", "lte", "gte"]
    }
    ordering = ['-timestamp']
    ordering_fields = ['timestamp']
