from django.db.models import Model
from django.utils.translation import gettext_lazy as _
from plans.models import (
    Approval,
    Plan as PlanModel,
    PlanConfigurationBooleanItem,
    PlanConfigurationIntegerItem,
)
from exceptions.core import FreePlanNotFoundError

class PlanSettings:
    DEFAULTS = {
        "mails": 2,
        "allow_custom_redirect": False,
    }

    def __init__(self, plan: PlanModel):
        self.mails = self.DEFAULTS["mails"]
        self.allow_custom_redirect = self.DEFAULTS["allow_custom_redirect"]

        mails_model = PlanConfigurationIntegerItem.objects.filter(plan=plan, name__iexact="mails").first()
        if mails_model:
            self.mails = mails_model.value
        
        allow_custom_redirect_model = PlanConfigurationBooleanItem.objects.filter(
            plan=plan,
            name__iexact="allow_custom_redirect"
        ).first()
        if allow_custom_redirect_model:
            self.allow_custom_redirect = allow_custom_redirect_model.value

class Plan:
    def get_best_approval(self, approvals: list):
        if len(approvals) == 0:
            return None
        current_approval = approvals[0]
        for approval in approvals:
            if approval.plan.monthly_price >= current_approval.plan.monthly_price:
                current_approval = approval
        return current_approval

    def __init__(self, user: Model) -> None:
        self.user = user
        approvals = list(
            Approval.objects.filter(
                user=user,
                status=Approval.STATUS_ACTIVE,
            ).all()
        )
        self.approval = self.get_best_approval(approvals)

        if not self.approval:
            free_plan = PlanModel.objects.filter(plan_type=PlanModel.TYPE_FREE).first()
            if not free_plan:
                raise FreePlanNotFoundError()
            
            self.approval = Approval.objects.create(
                user=user,
                plan=free_plan,
                status=Approval.STATUS_ACTIVE,
            )
        
        self.plan = self.approval.plan
        self.settings = PlanSettings(self.plan)

    def is_paid_approval(self):
        if not self.approval:
            return False
        return self.approval.plan.plan_type == PlanModel.TYPE_PAID
