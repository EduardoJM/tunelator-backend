from rest_framework import serializers
from content.models import SocialContent

class SocialContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialContent
        fields = "__all__"
