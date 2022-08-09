from django.contrib import admin
from content.models import SocialContent

@admin.register(SocialContent)
class SocialContentAdmin(admin.ModelAdmin):
    list_display = ["type", "title", "created_at", "updated_at"]
    fields = ["type", "title", "description", "link", "image"]
