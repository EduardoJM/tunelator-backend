from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from mirage import fields as mirage_fields
from plans.plan import Plan
from mails.validators import UserMailAliasValidator

User = get_user_model()

class UserMail(models.Model):
    mail_user_validator = UserMailAliasValidator()

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
        max_length=25,
        validators = [mail_user_validator],
    )
    mail = models.CharField(
        _("mail"),
        max_length=255,
        null=True,
        blank=True,
        default=None,
    )
    redirect_enabled = models.BooleanField(
        _("redirect enabled"),
        default=True
    )
    redirect_to = models.EmailField(
        _("redirect to e-mail"),
        blank=True,
        null=True,
        default=None
    )
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _("updated at"),
        auto_now=True
    )
    plan_enabled = models.BooleanField(
        _("plan enabled"),
        default=True
    )

    def full_clean(self, exclude=None, validate_unique=True):
        self.mail_user = str(self.mail_user).lower()

        mails_count = len(
            UserMail.objects.filter(user=self.user).all()
        )
        plan = Plan(self.user)

        if self.redirect_to and not plan.settings.allow_custom_redirect:
            raise ValidationError(_('your plan not have custom redirects.'))

        if str(self.redirect_to).lower().endswith('@tunelator.com.br'):
            raise ValidationError(_("you can't redirect to other tunelator e-mail."))
        
        if mails_count >= plan.settings.mails:
            raise ValidationError(_('you reached the limit of mails for your plan.'))
        
        return super(UserMail, self).full_clean(exclude=exclude, validate_unique=validate_unique)

    def save(self, *args, **kwargs):
        super(UserMail, self).save(*args, **kwargs)

        if self.mail_user and not self.mail:
            from mails.tasks import create_mail_user
            create_mail_user.apply_async(args=[self.pk], countdown=2)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _("user mail")
        verbose_name_plural = _("user mails")

class UserReceivedMail(models.Model):
    mail = models.ForeignKey(
        UserMail,
        verbose_name=_("mail"),
        related_name="received",
        on_delete=models.CASCADE
    )
    origin_mail = models.CharField(_("origin mail"), blank=True, null=True, max_length=255, default="")
    subject = models.CharField(_("subject"), blank=True, null=True, max_length=255, default="")
    date = models.DateTimeField(_("date"), auto_now_add=True)
    raw_file_path = models.TextField(_("raw file path"), blank=True, null=True, default=None)
    raw_mail = mirage_fields.EncryptedTextField()
    delivered = models.BooleanField(_("delivered"), default=False)
    delivered_date = models.DateTimeField(_('delivered date'), null=True, default=None)

    def save(self, *args, **kwargs):
        super(UserReceivedMail, self).save(*args, **kwargs)

        if not self.delivered:
            from mails.tasks import send_redirect_mail
            send_redirect_mail.apply_async(args=[self.pk], countdown=2)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = _("User Received Email")
        verbose_name_plural = _("User Received Emails")
