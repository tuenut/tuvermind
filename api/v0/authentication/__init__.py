from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTAuthenticationWithCookie(JWTAuthentication):
    def authenticate(self, request):
        print("!!! JWTAuthenticationWithCookie !!!")

        raw_token = request._request.COOKIES.get("drfjwt_access_token", None)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        return self.get_user(validated_token), validated_token
