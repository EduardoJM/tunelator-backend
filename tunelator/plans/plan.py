from django.db.models import Model
from django.utils.translation import gettext_lazy as _
from plans.models import (
    Approval,
    Plan as PlanModel,
    PlanConfigurationIntegerItem,
)

class PlanSettings:
    DEFAULTS = {
        "mails": 2,
    }

    def __init__(self, plan: PlanModel):
        self.mails = self.DEFAULTS["mails"]

        mails_model = PlanConfigurationIntegerItem.objects.filter(plan=plan, name__iexact="mails").first()
        if mails_model:
            self.mails = mails_model.value

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
                status=Approval.STATUS_AUTHORIZED,
            ).all()
        )
        self.approval = self.get_best_approval(approvals)

        if not self.approval:
            free_plan = PlanModel.objects.filter(plan_type=PlanModel.TYPE_FREE).first()
            if not free_plan:
                raise Exception(_("Free plan not found for attribution"))
            
            self.approval = Approval.objects.create(
                user=user,
                plan=free_plan,
                status=Approval.STATUS_AUTHORIZED,
            )
        
        self.plan = self.approval.plan
        self.settings = PlanSettings(self.plan)
