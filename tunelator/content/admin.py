from django.contrib import admin
from content.models import SocialContent, SocialContentType
from content.forms import SocialContentForm

@admin.register(SocialContentType)
class SocialContentTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    fields = ["name"]

@admin.register(SocialContent)
class SocialContentAdmin(admin.ModelAdmin):
    list_display = ["type", "title", "created_at", "updated_at"]
    fields = ["type", "title", "description", "link", "image"]
    form = SocialContentForm
