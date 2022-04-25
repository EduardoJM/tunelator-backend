from rest_framework import serializers
from payments.models import SubscriptionCheckout, SubscriptionManager

class SubscriptionCheckoutSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SubscriptionCheckout
        fields = ["user", "plan"]

class SubscriptionCheckoutRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionCheckout
        fields = ["checkout_id"]

class SubscriptionManagerSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SubscriptionManager
        fields = ["user"]

class SubscriptionManagerRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionManager
        fields = ["manager_id"]
