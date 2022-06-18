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
from django.conf.urls.static import static

import settings
import settings.paths
from api import urls as api_urls

# Routers provide an easy way of automatically determining the URL conf.


favicon_path = re_path(
    r'^favicon\.ico$',
    RedirectView.as_view(url='/static/images/favicon.ico'),
    name='favicon'
)

# auth_url = url(
#     r'api/auth',
#     include('rest_framework.urls', namespace='rest_framework')
# )

admin_path = path('admin/', admin.site.urls)
api_path = path('api/', include(api_urls))

urlpatterns = [
    favicon_path,
    admin_path,
    api_path,
    # auth_url,
]
urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.paths.MEDIA_ROOT))

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
        *urlpatterns,
    ]
