"""tuvermind URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import RedirectView
from django.conf.urls import url, include

from rest_framework import routers

from api.v0.weather.urls import router as weather_router, urlpatterns as weather_urls
from api.v0.authentication.urls import urlpatterns as auth_urls

# Routers provide an easy way of automatically determining the URL conf.

router = routers.DefaultRouter()
router.registry.extend(weather_router.registry)

favicon_path = re_path(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico'), name='favicon')

urlpatterns = [
    favicon_path,
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    url(r'api/auth', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns.extend(weather_urls)
urlpatterns.extend(auth_urls)
