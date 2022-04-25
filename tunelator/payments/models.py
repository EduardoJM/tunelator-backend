import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from plans.models import Plan

User = get_user_model()

class SubscriptionManager(models.Model):
    manager_id = models.CharField(verbose_name=_('checkout id'), max_length=50)
    user = models.ForeignKey(User, verbose_name=_('user'), on_delete=models.CASCADE)
    used = models.BooleanField(_('used'), default=False)

    def __str__(self):
        return self.manager_id
    
    def save(self, *args, **kwargs):
        if not self.manager_id:
            self.manager_id = str(uuid.uuid4())
        return super(SubscriptionManager, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = _('Subscription manager ID')
        verbose_name_plural = _('Subscription managers ID')

class SubscriptionCheckout(models.Model):
    checkout_id = models.CharField(verbose_name=_('checkout id'), max_length=50)
    user = models.ForeignKey(User, verbose_name=_('user'), on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, verbose_name=_('plan'), on_delete=models.CASCADE)
    used = models.BooleanField(_('used'), default=False)

    def __str__(self):
        return self.checkout_id

    def save(self, *args, **kwargs):
        if not self.checkout_id:
            self.checkout_id = str(uuid.uuid4())
        super(SubscriptionCheckout, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Subscription checkout ID')
        verbose_name_plural = _('Subscription checkouts ID')
