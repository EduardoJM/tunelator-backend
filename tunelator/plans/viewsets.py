from rest_framework import viewsets, mixins, decorators, response, status
from django.utils.translation import gettext_lazy as _
from mails.models import UserMail
from plans.models import Plan
from plans.serializers import PlanSerializer, ActivePlanSerializer
from plans.plan import Plan as PlanUtil

class PlanViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Plan.objects.filter(is_visible=True)
    serializer_class = PlanSerializer
    permission_classes = []
    pagination_class = None

    @decorators.action(detail=False, methods=["GET"])
    def active(self, request):
        if not request.user.is_authenticated:
            return response.Response(
                { 'detail': _('user is not authenticated.') },
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        plan_util = PlanUtil(request.user)
        approval = plan_util.approval
        plan = approval.plan

        max_mails_count = plan_util.settings.mails
        current_mails_count = len(
            UserMail.objects.filter(user=request.user).all()
        )
        free_accounts = max_mails_count - current_mails_count
        if free_accounts < 0:
            free_accounts = 0

        serializer = ActivePlanSerializer(instance=plan)
        data = {
            **serializer.data,
            'free_accounts': free_accounts
        }
        return response.Response(data)
