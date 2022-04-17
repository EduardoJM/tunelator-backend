from django.contrib import admin
from mails.models import UserMail, UserReceivedMail, UserReceivedMailAttachment

@admin.register(UserMail)
class UserMailAdmin(admin.ModelAdmin):
    list_display = ["user", "name", "mail_user", "mail", "redirect_enabled", "created_at"]
    fields = ["user", "name", "mail_user", "redirect_enabled"]

@admin.register(UserReceivedMail)
class UserReceivedMailAdmin(admin.ModelAdmin):
    list_display = ["mail", "origin_mail", "subject", "date", "delivered", "delivered_date"]

@admin.register(UserReceivedMailAttachment)
class UserReceivedMailAttachmentAdmin(admin.ModelAdmin):
    list_display = ["received_mail", "file_name", "file"]
