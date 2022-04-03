from rest_framework import viewsets, mixins
from plans.models import Plan
from plans.serializers import PlanSerializer

class PlanViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Plan.objects.filter(is_visible=True)
    serializer_class = PlanSerializer
    permission_classes = []
