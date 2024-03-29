from rest_framework import serializers
from mails.models import UserMail, UserReceivedMail
from mails.validators import UserMailAliasValidator

class UserReceivedMailInternSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMail
        fields = ["id", "mail", "redirect_to"]

class UserReceivedMailSerializer(serializers.ModelSerializer):
    mail = UserReceivedMailInternSerializer()

    class Meta:
        model = UserReceivedMail
        fields = ["id", "mail", "origin_mail", "subject", "date", "delivered", "delivered_date"]

class UserMailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserMail
        fields = ["user", "name", "mail_user", "redirect_enabled", "redirect_to"]

class UserMailRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMail
        fields = ["id", "name", "mail", "mail_user", "redirect_enabled", "redirect_to", "plan_enabled", "created_at", "updated_at"]

mail_user_validator = UserMailAliasValidator()

class UserMailVerifySerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=25, validators=[mail_user_validator])
