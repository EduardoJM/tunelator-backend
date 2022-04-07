from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from system import linux_user

User = get_user_model()

class UserMail(models.Model):
    user = models.ForeignKey(
        User,
        related_name="mails",
        verbose_name=_("user"),
        on_delete=models.CASCADE
    )
    name = models.CharField(
        _("name"),
        max_length=100,
    )
    mail_user = models.CharField(
        _("mail user"),
        max_length=32,
        null=True,
        default=None,
    )
    mail = models.CharField(
        _("mail"),
        max_length=255,
        null=True,
        default=None,
    )
    redirect_enabled = models.BooleanField(
        _("redirect enabled"),
        default=True
    )
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _("updated at"),
        auto_now=True
    )

    def full_clean(self, exclude=None, validate_unique=True):
        ## TODO: verify if user (plan) has permission to made that action
        return super(UserMail, self).full_clean(exclude=exclude, validate_unique=validate_unique)

    def save(self, *args, **kwargs):
        if self.mail_user and not self.mail:
            self.mail = "%s@tunelator.com.br" % self.mail_user

        super(UserMail, self).save(*args, **kwargs)

        if not self.mail_user:
            from mails.tasks import create_mail_user
            create_mail_user.apply_async(args=[self.pk], countdown=2)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _("user mail")
        verbose_name_plural = _("user mails")
