from django.urls import path, include
from rest_framework import routers

from api.v0.weather.views import WeatherTypesViewSet, WeatherViewSet
from api.swagger import urlpatterns as swagger_urls

app_name = 'api_v0'

router = routers.DefaultRouter()

router.register(r'weather/types', WeatherTypesViewSet)
router.register(r'weather', WeatherViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(swagger_urls)),
]
