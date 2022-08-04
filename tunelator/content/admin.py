from django.contrib import admin
from content.models import SocialContent

@admin.register(SocialContent)
class SocialContentAdmin(admin.ModelAdmin):
    list_display = ["title", "created_at", "updated_at"]
    fields = ["title", "description", "link", "image"]
