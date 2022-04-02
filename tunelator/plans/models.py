from django.db import models
from django.utils.translation import gettext_lazy as _
from polymorphic.models import PolymorphicModel

class Plan(models.Model):
    name = models.CharField(_("name"), max_length=150)
    description = models.TextField(_("description"))

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _("plan")
        verbose_name_plural = _("plans")

class PlanDisplayFeature(models.Model):
    plan = models.ForeignKey(
        Plan, related_name="display_features", on_delete=models.CASCADE, verbose_name=_("plan")
    )
    enabled = models.BooleanField(_("enabled"), default=True)
    name = models.CharField(_("name"), max_length=150)

    def __str__(self):
        return self.name

    class Meta:
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
