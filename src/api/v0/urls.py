from django.urls import path, include

from rest_framework import routers

from api.v0.weather.views import WeatherTypesViewSet, WeatherViewSet
from api.v0.todoes.views import TodoTaskViewSet
from api.v0.authentication.views import (
    TokenObtainPairSetCookieView, TokenRefreshView, TokenVerifyCustomView
)
from api.swagger import urlpatterns as swagger_urls

app_name = 'api_v0'

router = routers.DefaultRouter()

router.register(r'weather/types', WeatherTypesViewSet)
router.register(r'weather', WeatherViewSet)
router.register(r'todo', TodoTaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'token/',
        TokenObtainPairSetCookieView.as_view(),
        name='token_obtain_pair'
    ),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(
        'token/verify/',
        TokenVerifyCustomView.as_view(),
        name='token_verify'
    ),

    path('', include(swagger_urls)),
]
