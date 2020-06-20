from rest_framework import routers

from apps.openweathermap.api.views import WeatherTypesViewSet, WeatherHistoryViewSet

router = routers.SimpleRouter()

router.register(r'weather/types', WeatherTypesViewSet)
router.register(r'weather', WeatherHistoryViewSet)