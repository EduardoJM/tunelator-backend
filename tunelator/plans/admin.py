from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from polymorphic.admin import (
    PolymorphicParentModelAdmin,
    PolymorphicChildModelAdmin,
    PolymorphicChildModelFilter,
    PolymorphicInlineSupportMixin,
    StackedPolymorphicInline
)
from adminsortable.admin import SortableTabularInline, NonSortableParentAdmin
from plans.models import (
    Plan,
    PlanConfigurationStringItem,
    PlanDisplayFeature,
    PlanConfigurationItem,
    PlanConfigurationBooleanItem,
    Approval,
)

class PlanConfigurationItemAdmin(PolymorphicChildModelAdmin):
    base_model = PlanConfigurationItem

@admin.register(PlanConfigurationBooleanItem)
class PlanConfigurationBooleanItemAdmin(PlanConfigurationItemAdmin):
    base_modal = PlanConfigurationBooleanItem
    show_in_index = False

@admin.register(PlanConfigurationStringItem)
class PlanConfigurationStringItemAdmin(PlanConfigurationItemAdmin):
    base_model = PlanConfigurationStringItem
    show_in_index = False

@admin.register(PlanConfigurationItem)
class PlanConfigurationItemAdmin(PolymorphicParentModelAdmin):
    base_model = PlanConfigurationItem
    child_models = (
        PlanConfigurationBooleanItem,
        PlanConfigurationStringItem,
    )
    list_filter = (PolymorphicChildModelFilter,)
    list_display = ['id', 'plan', 'name', 'display_value']

    def display_value(self, obj):
        if hasattr(obj, 'value'):
            return str(getattr(obj, 'value'))
        return '-'
    display_value.short_description = _('value')

class PlanDisplayFeatureInlineAdmin(SortableTabularInline):
    model = PlanDisplayFeature
    extra = 0

class PlanConfigurationItemInline(StackedPolymorphicInline):
    class PlanConfigurationStringItemInline(StackedPolymorphicInline.Child):
        model = PlanConfigurationStringItem
    
    class PlanConfigurationBooleanItemInline(StackedPolymorphicInline.Child):
        model = PlanConfigurationBooleanItem
    
    model = PlanConfigurationItem
    child_inlines = (
        PlanConfigurationStringItemInline,
        PlanConfigurationBooleanItemInline,
    )

@admin.register(Plan)
class PlanAdmin(PolymorphicInlineSupportMixin, NonSortableParentAdmin):
    inlines = (PlanConfigurationItemInline, PlanDisplayFeatureInlineAdmin)

@admin.register(Approval)
class ApprovalAdmin(admin.ModelAdmin):
    list_display = ["user", "plan", "approval_id", "status"]
