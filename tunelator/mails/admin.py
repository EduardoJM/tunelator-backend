from django.contrib import admin
from mails.models import UserMail

@admin.register(UserMail)
class UserMailAdmin(admin.ModelAdmin):
    list_display = ["user", "name", "mail_user", "mail", "redirect_enabled", "created_at"]
    fields = ["user", "name", "redirect_enabled"]
