from django.contrib import admin
from mails.models import UserMail, UserReceivedMail

@admin.register(UserMail)
class UserMailAdmin(admin.ModelAdmin):
    list_display = ["user", "name", "mail_user", "mail", "redirect_enabled", "created_at"]
    fields = ["user", "name", "redirect_enabled"]

@admin.register(UserReceivedMail)
class UserReceivedMailAdmin(admin.ModelAdmin):
    list_display = ["mail", "origin_mail", "subject", "date", "delivered", "delivered_date"]
