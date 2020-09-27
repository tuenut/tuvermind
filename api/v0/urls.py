from rest_framework import routers

from api.v0.weather.views import WeatherTypesViewSet, WeatherViewSet
from api.v0.todoes.views import TodoTaskViewSet, ScheduledTodoTaskViewSet
from api.v0.todoes.timeintervals.views import IntervalsViewSet, CrontabViewsSet, ClockedViewsSet

router = routers.SimpleRouter()

router.register(r'weather/types', WeatherTypesViewSet)
router.register(r'weather', WeatherViewSet)
router.register(r'todo/interval', IntervalsViewSet)
router.register(r'todo/crontab', CrontabViewsSet)
router.register(r'todo/clocked', ClockedViewsSet)
router.register(r'todo/scheduled', ScheduledTodoTaskViewSet)
router.register(r'todo', TodoTaskViewSet)


urlpatterns = []
