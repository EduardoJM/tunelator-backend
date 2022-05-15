from rest_framework.schemas.openapi import AutoSchema
from rest_framework import serializers
from authentication.serializers import AuthenticationUserSerializer

class TokenObtainPairRequestSchemaSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

class TokenObtainPairResponseSchemaSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = AuthenticationUserSerializer(read_only=True)

class UserCreateViewSchemaRequestSchemaSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

class TokenObtainPairViewSchema(AutoSchema):
    def get_request_serializer(self, path, method):
        return TokenObtainPairRequestSchemaSerializer()
    
    def get_response_serializer(self, path, method):
        return TokenObtainPairResponseSchemaSerializer()

    def get_responses(self, path, method):
        data = super().get_responses(path, method)

        if "201" in data:
            item = data["201"]
            del data["201"]
            data["200"] = item

        return data

class UserCreateViewSchema(AutoSchema):
    def get_response_serializer(self, path, method):
        return TokenObtainPairResponseSchemaSerializer()

    def get_request_serializer(self, path, method):
        return UserCreateViewSchemaRequestSchemaSerializer()