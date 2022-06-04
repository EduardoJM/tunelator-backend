from django.contrib.auth import get_user_model
from django.utils import timezone
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
    ForgotPasswordSessionSerializer,
    ForgotPasswordSessionResetSerializer,
)
from authentication.models import ForgotPasswordSession
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

class ForgotPasswordSessionView(APIView):
    permission_classes = []
    authentication_classes = []

    @swagger_auto_schema(
        request_body=ForgotPasswordSessionSerializer,
        responses={
            status.HTTP_200_OK: "No body",
        },
        security=[],
    )
    def post(self, request):
        from authentication.tasks import send_recovery_link
        
        serializer = ForgotPasswordSessionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        send_recovery_link.delay(serializer.validated_data['email'])

        return Response(status=status.HTTP_200_OK)

class ForgotPasswordValidateSessionView(APIView):
    permission_classes = []
    authentication_classes = []

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: "No body. Indicates that the session is valid.",
            status.HTTP_404_NOT_FOUND: "No body. Indicates that the session is not found.",
            status.HTTP_422_UNPROCESSABLE_ENTITY: 'No body. Indicates that the session is expired.',
        },
        security=[],
    )
    def get(self, request, session_id):
        session = ForgotPasswordSession.objects.filter(session_id=session_id).first()
        if not session:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if session.used:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if timezone.now() > session.valid_until:
            session.used = True
            session.save()
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return Response(status=status.HTTP_200_OK)

class ForgotPasswordSessionResetView(APIView):
    permission_classes = []
    authentication_classes = []
    
    @swagger_auto_schema(
        request_body=ForgotPasswordSessionResetSerializer,
        responses={
            status.HTTP_200_OK: "No body. Indicates that the user password was changed.",
            status.HTTP_404_NOT_FOUND: "No body. Indicates that the session is not found.",
            status.HTTP_422_UNPROCESSABLE_ENTITY: 'No body. Indicates that the session is expired.',
        },
        security=[],
    )
    def put(self, request, session_id):
        session = ForgotPasswordSession.objects.filter(session_id=session_id).first()
        if not session:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if session.used:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if timezone.now() > session.valid_until:
            session.used = True
            session.save()
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        serializer = ForgotPasswordSessionResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = session.user
        user.set_password(serializer.validated_data['password'])
        session.used = True
        session.save()
        user.save()

        return Response(status=status.HTTP_200_OK)
