from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer
from plans.models import (
    Plan,
    PlanDisplayFeature,
    PlanConfigurationItem,
    PlanConfigurationIntegerItem,
    PlanConfigurationBooleanItem,
    PlanConfigurationStringItem,
)
from mails.models import UserMail

class PlanDisplayFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanDisplayFeature
        fields = ["name", "enabled"]

class PlanSerializer(serializers.ModelSerializer):
    display_features = PlanDisplayFeatureSerializer(many=True)

    class Meta:
        model = Plan
        exclude = ["is_visible", "stripe_price_id"]

class PlanConfigurationIntegerItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanConfigurationIntegerItem
        fields = ["name", "value"]

class PlanConfigurationBooleanItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanConfigurationBooleanItem
        fields = ["name", "value"]

class PlanConfigurationStringItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanConfigurationStringItem
        fields = ["name", "value"]

class PlanConfigurationItem(PolymorphicSerializer):
    model_serializer_mapping = {
        PlanConfigurationIntegerItem: PlanConfigurationIntegerItemSerializer,
        PlanConfigurationBooleanItem: PlanConfigurationBooleanItemSerializer,
        PlanConfigurationStringItem: PlanConfigurationStringItemSerializer
    }

class ActivePlanSerializer(serializers.ModelSerializer):
    configs = PlanConfigurationItem(many=True)
    display_features = PlanDisplayFeatureSerializer(many=True)
    free_accounts = serializers.SerializerMethodField()

    def get_free_accounts(self, plan):
        return 0

    class Meta:
        model = Plan
        exclude = ["is_visible", "stripe_price_id"]

