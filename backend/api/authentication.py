# authentication.py
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User

class CookieJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('access')
        if not token:
            return None

        try:
            validated_token = AccessToken(token)
            user = User.objects.get(id=validated_token['user_id'])
            return (user, None)
        except Exception:
            raise AuthenticationFailed('Invalid or expired token')
