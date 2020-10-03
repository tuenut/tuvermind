from rest_framework import routers

from api.v0.weather.views import WeatherTypesViewSet, WeatherViewSet
from api.v0.todoes.views import TodoTaskViewSet, ScheduledTodoTaskViewSet


router = routers.SimpleRouter()

router.register(r'weather/types', WeatherTypesViewSet)
router.register(r'weather', WeatherViewSet)
router.register(r'todo/scheduled', ScheduledTodoTaskViewSet)
router.register(r'todo', TodoTaskViewSet)


urlpatterns = []
