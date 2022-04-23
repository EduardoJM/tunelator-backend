from rest_framework import serializers
from payments.models import SubscriptionCheckout

class SubscriptionCheckoutSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SubscriptionCheckout
        fields = ["user", "plan"]

class SubscriptionCheckoutRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionCheckout
        fields = ["checkout_id"]
