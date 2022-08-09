from rest_framework import serializers
from content.models import SocialContent

class SocialContentSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    def get_type(self, social_content):
        return social_content.type.name

    class Meta:
        model = SocialContent
        fields = "__all__"
