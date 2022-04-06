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
    )
    mail = models.CharField(
        _("mail"),
        max_length=255,
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

    def _generate_email(self):
        self.mail_user = linux_user.get_unique_name(self.name)
        if not linux_user.create_mail_anonymous_user(self.mail_user):
            raise ValidationError(_("we have a problem saving your mail. try again later."))
        self.mail = "%s@%s" % (self.mail_user, "tunelator.com.br")

    def full_clean(self, exclude=None, validate_unique=True):
        ## TODO: verify if user (plan) has permission to made that action

        self._generate_email()
        return super(UserMail, self).full_clean(exclude=exclude, validate_unique=validate_unique)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _("user mail")
        verbose_name_plural = _("user mails")
