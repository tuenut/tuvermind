from web.apps.openweathermap.api.views import WeatherTypesViewSet, WeatherHistoryViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'types', WeatherTypesViewSet)
router.register(r'history', WeatherHistoryViewSet)
