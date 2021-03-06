from rest_framework import routers

from api.v0.weather.views import WeatherTypesViewSet, WeatherViewSet

router = routers.SimpleRouter()

router.register(r'weather/types', WeatherTypesViewSet)
router.register(r'weather', WeatherViewSet)

urlpatterns = []
