from django.urls import include, path
from django.conf.urls import url

from api.v0 import urls as api_v0_urls


urlpatterns = [
    url(r'v0/', include(api_v0_urls, namespace="v0")),
]
