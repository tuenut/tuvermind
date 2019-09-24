from django.shortcuts import render
from django.views import generic
from django.utils import timezone

from web.apps.openweathermap.models import OWMData


# Create your views here.


class WeatherView(generic.ListView):
    template_name = "weather/index.html"
    context_object_name = 'weather'

    def get_queryset(self):
        data = OWMData.objects.filter(
            timestamp__gte=timezone.now().date(),
            timestamp__hour__in=[0, 6, 9, 12, 15, 6, 9]
        )

        groups = sorted(list({item.timestamp.date() for item in data}))

        return {'groups': groups, 'data': data}
