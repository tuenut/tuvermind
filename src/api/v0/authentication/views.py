from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from . import JWTAuthenticationWithCookie, JWTAuthentication


class TokenObtainPairSetCookieView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            refresh_token = response.data['refresh']
            access_token = response.data['access']

            response.set_cookie("drfjwt_refresh_token", refresh_token, samesite="lax", httponly=True)
            response.set_cookie("drfjwt_access_token", access_token, samesite="lax", httponly=True)

        return response


class TokenVerifyCustomView(TokenVerifyView):
    authentication_classes = [JWTAuthentication, JWTAuthenticationWithCookie]
    permission_classes = [AllowAny, ]

    def get(self, request, *args, **kwargs):
        return Response({
            'userName': str(request.user),
            'message': "Verified by cookie." if not isinstance(request.user, AnonymousUser) else "Unauthenticated!"

        })
