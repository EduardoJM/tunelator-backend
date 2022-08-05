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

TYPE_SESSION_COMPLETE = "checkout.session.completed"
TYPE_SUBSCRIPTION_UPDATE = "customer.subscription.updated"
TYPE_SUBSCRIPTION_DELETED = "customer.subscription.deleted"
TYPES = (
    (TYPE_SESSION_COMPLETE, "Session Completed"),
    (TYPE_SUBSCRIPTION_UPDATE, "Subscription Updated"),
    (TYPE_SUBSCRIPTION_DELETED, "Subscription Deleted")
)

class WebhookWaitedFieldsSerializer(serializers.Serializer):
    class WebhookDataSerializer(serializers.Serializer):
        class WebhookDataObjectSerializer(serializers.Serializer):
            id = serializers.CharField()
            subscription = serializers.CharField()
            customer = serializers.CharField()
            status = serializers.CharField()

        object = WebhookDataObjectSerializer()

    data = WebhookDataSerializer()
    type = serializers.ChoiceField(choices=TYPES)
