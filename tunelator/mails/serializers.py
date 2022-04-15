from rest_framework import serializers
from mails.models import UserMail

class UserMailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserMail
        fields = ["user", "name", "redirect_enabled"]

class UserMailRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMail
        fields = ["id", "name", "mail", "redirect_enabled", "plan_enabled", "created_at", "updated_at"]
