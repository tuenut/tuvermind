from django.urls import path

from .views import TokenObtainPairSetCookieView, TokenRefreshView, TokenVerifyCustomView

urlpatterns = [
    path('api/token/', TokenObtainPairSetCookieView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyCustomView.as_view(), name='token_verify'),
]
