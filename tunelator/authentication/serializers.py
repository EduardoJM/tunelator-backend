from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as BaseTokenObtainPairSerializer,
)

User = get_user_model()

class AuthenticationUserUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
        ]

class AuthenticationUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "date_joined",
            "last_login",
        ]

class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()

    def validate_email(self, value):
        if User.objects.filter(email=value).first():
            raise ValidationError(_('The e-mail is already used.'))
        return value

class TokenObtainPairSerializer(BaseTokenObtainPairSerializer):
    def get_user_data(self):
        user_serializer = AuthenticationUserSerializer(self.user)
        return user_serializer.data

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["user"] = self.get_user_data()

        update_last_login(None, self.user)

        return data

class ForgotPasswordSessionSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ForgotPasswordSessionResetSerializer(serializers.Serializer):
    password = serializers.CharField()

#
# Schema Utils
#
class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = AuthenticationUserSerializer(read_only=True)

class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    user = AuthenticationUserSerializer(read_only=True)
