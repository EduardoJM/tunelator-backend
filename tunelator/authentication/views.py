from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView as BaseTokenObtainPairView,
    TokenRefreshView as BaseTokenRefreshView,
)
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from authentication.serializers import TokenObtainPairSerializer, AuthenticationUserSerializer

class TokenObtainPairView(BaseTokenObtainPairView):
    def get_serializer_class(self):
        return TokenObtainPairSerializer

class TokenRefreshView(BaseTokenRefreshView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        token = AccessToken(serializer.validated_data["access"])
        auth = JWTAuthentication()
        user = auth.get_user(token)
        user_serializer = AuthenticationUserSerializer(
            instance=user, context={"request": request}
        )

        data = {**serializer.validated_data, "user": user_serializer.data}
        return Response(data)
