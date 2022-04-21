from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from polymorphic.models import PolymorphicModel
from adminsortable.models import SortableMixin

User = get_user_model()

class Plan(models.Model):
    TYPE_FREE = "free"
    TYPE_PAID = "paid"
    TYPES = (
        (TYPE_FREE, _("Free")),
        (TYPE_PAID, _("Paid")),
    )

    name = models.CharField(_("name"), max_length=150)
    description = models.TextField(_("description"))
    is_visible = models.BooleanField(_("plan is visible"), default=True)
    plan_type = models.CharField(_("plan type"), max_length=10, choices=TYPES, default=TYPE_PAID)
    monthly_price = models.IntegerField(_("monthly price"), default=999)
    mp_plan_id = models.CharField(_("mercado pago integration id"), max_length=255, blank=True, default="")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _("plan")
        verbose_name_plural = _("plans")

class PlanDisplayFeature(SortableMixin):
    plan = models.ForeignKey(
        Plan, related_name="display_features", on_delete=models.CASCADE, verbose_name=_("plan")
    )
    the_order = models.PositiveIntegerField(_('order'), default=0, editable=False, db_index=True)
    enabled = models.BooleanField(_("enabled"), default=True)
    name = models.CharField(_("name"), max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['the_order']
        verbose_name = _("plan display feature")
        verbose_name_plural = _("plan display features")

class PlanConfigurationItem(PolymorphicModel):
    plan = models.ForeignKey(
        Plan, related_name="configs", on_delete=models.CASCADE, verbose_name=_("plan")
    )
    name = models.CharField(_('name'), max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('plan configuration item')
        verbose_name_plural = _('plan configuration items')

class PlanConfigurationBooleanItem(PlanConfigurationItem):
    value = models.BooleanField(_('value'), default=True)

    class Meta:
        verbose_name = _('plan configuration boolean item')
        verbose_name_plural = _('plan configuration boolean items')

class PlanConfigurationStringItem(PlanConfigurationItem):
    value = models.CharField(_('value'), max_length=150, blank=True, default='')

    class Meta:
        verbose_name = _('plan configuration string item')
        verbose_name_plural = _('plan configuration string items')

class PlanConfigurationIntegerItem(PlanConfigurationItem):
    value = models.IntegerField(_('value'), default=0)

    class Meta:
        verbose_name = _('plan configuration integer item')
        verbose_name_plural = _('plan configuration integer items')

class Approval(models.Model):
    STATUS_AUTHORIZED = "authorized"
    STATUS_PAUSED = "paused"
    STATUS_PENDING = "pending"
    STATUS_CANCELLED = "cancelled"
    STATUS = (
        (STATUS_AUTHORIZED, _("Authorized")),
        (STATUS_PAUSED, _("Paused")),
        (STATUS_PENDING, _("Pending")),
        (STATUS_CANCELLED, _("Cancelled")),
    )

    user = models.ForeignKey(User, related_name="approvals", on_delete=models.CASCADE, verbose_name=_("user"))
    plan = models.ForeignKey(Plan, verbose_name=_("plan"), related_name="subscriptions", on_delete=models.CASCADE)
    approval_id = models.CharField(_('approval id'), max_length=255, blank=True, null=True)
    status = models.CharField(_("status"), max_length=20, choices=STATUS, default=STATUS_PENDING)

    def __str__(self):
        return _('approval of %(user)s to plan %(plan)s') % {
            'user': str(self.user),
            'plan': str(self.plan),
        }

    class Meta:
        verbose_name = _("Approval")
        verbose_name_plural = _("Approvals")

