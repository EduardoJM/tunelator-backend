from rest_framework import viewsets, mixins, decorators, response, status
from django.utils.translation import gettext_lazy as _
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
                status=status.HTTP_403_UNAUTHORIZED
            )
        
        plan_util = PlanUtil(request.user)
        approval = plan_util.approval
        plan = approval.plan

        serializer = ActivePlanSerializer(instance=plan)
        return response.Response(serializer.data)
