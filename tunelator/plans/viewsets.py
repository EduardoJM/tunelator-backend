import json
import requests
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets, mixins, decorators, response, status
from plans.models import Plan, Approval
from plans.serializers import PlanSerializer, PlanApprovalSerializer

class PlanViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Plan.objects.filter(is_visible=True)
    serializer_class = PlanSerializer
    permission_classes = []

    @decorators.action(detail=True, methods=["POST"])
    def approval(self, request, pk):
        # TODO: validate if authenticated user has a plan
        if not request.user.is_authenticated:
            return response.Response({
                "detail": "you are not authenticated"
            }, status=status.HTTP_401_UNAUTHORIZED)

        serializer = PlanApprovalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.data

        approval = Approval()
        approval.user = request.user
        approval.plan = self.get_object()
        approval.save()

        payload = {
            "preapproval_plan_id": approval.plan.mp_plan_id,
            "card_token_id": data["card_token_id"],
            "payer_email": "test_user_79075495@testuser.com",
        }
        headers = {
            "Authorization": "Bearer APP_USR-7029564028727729-040317-ca924e9519a29602294a56aea11284bf-1100657934",
            "Content-Type": "application/json",
        }
        mp_response = requests.post("https://api.mercadopago.com/preapproval", headers=headers, json=payload)

        print(mp_response.text)
        if mp_response.status_code == 201:
            output_data = json.loads(mp_response.text)
            if "id" in output_data:
                approval.approval_id = output_data["id"]
            if "status" in output_data:
                approval.status = output_data["status"]
            approval.save()

        return response.Response({
            "detail": _("Waiting for payment approval.")
        })
