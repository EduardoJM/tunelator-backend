from rest_framework import serializers
from plans.models import Plan, PlanDisplayFeature

class PlanDisplayFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanDisplayFeature
        fields = ["name", "enabled"]

class PlanSerializer(serializers.ModelSerializer):
    display_features = PlanDisplayFeatureSerializer(many=True)

    class Meta:
        model = Plan
        exclude = ["is_visible", "mp_plan_id"]

class PlanApprovalSerializer(serializers.Serializer):
    card_token_id = serializers.CharField()
