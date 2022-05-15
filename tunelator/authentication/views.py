from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView as BaseTokenObtainPairView,
    TokenRefreshView as BaseTokenRefreshView,
)
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from authentication.serializers import (
    TokenObtainPairSerializer,
    TokenObtainPairResponseSerializer,
    AuthenticationUserSerializer,
    AuthenticationUserUpdateSerializer,
    UserCreateSerializer,
    TokenRefreshResponseSerializer,
)
from drf_yasg.utils import swagger_auto_schema

User = get_user_model()

class UserProfileDataView(APIView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: AuthenticationUserSerializer,
        },
    )
    def get(self, request):
        serializer = AuthenticationUserSerializer(instance=request.user)
        return Response(serializer.data, status=200)
    
    @swagger_auto_schema(
        request_body=AuthenticationUserUpdateSerializer,
        responses={
            status.HTTP_200_OK: AuthenticationUserSerializer,
        },
    )
    def patch(self, request):
        serializer = AuthenticationUserUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        user = request.user
        user.__dict__.update(data)
        user.save()

        serializer = AuthenticationUserSerializer(instance=request.user)
        return Response(serializer.data, status=200)

class UserCreateView(APIView):
    permission_classes = []
    
    @swagger_auto_schema(
        request_body=UserCreateSerializer,
        responses={
            status.HTTP_201_CREATED: TokenObtainPairResponseSerializer,
        },
        security=[],
    )
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = User()
        user.email = data["email"]
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.set_password(data["password"])
        user.save()

        token_serializer = TokenObtainPairSerializer(data={
            "email": data["email"],
            "password": data["password"]
        })

        try:
            token_serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(token_serializer.validated_data, status=status.HTTP_201_CREATED)

class TokenObtainPairView(BaseTokenObtainPairView):
    def get_serializer_class(self):
        return TokenObtainPairSerializer
    
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenObtainPairResponseSerializer,
        },
        security=[],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class TokenRefreshView(BaseTokenRefreshView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenRefreshResponseSerializer,
        },
        security=[],
    )
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
