from django.contrib import admin
from mails.tasks import send_redirect_mail

@admin.action(description="Force redirect those e-mails")
def force_resend_mails(modeladmin, request, queryset):
    items = queryset.all()
    for item in items:
        send_redirect_mail.delay(item.pk, True)
