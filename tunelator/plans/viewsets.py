import json
import requests
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets, mixins, decorators, response, status
from plans.models import Plan, Approval
from plans.serializers import PlanSerializer, PlanApprovalSerializer

class PlanViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Plan.objects.filter(is_visible=True)
    serializer_class = PlanSerializer
    permission_classes = []
    pagination_class = None
