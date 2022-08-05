from rest_framework import serializers

class UnauthenticatedSerializer(serializers.Serializer):
    detail = serializers.CharField()
