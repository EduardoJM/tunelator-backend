from django.contrib import admin
from payments.models import SubscriptionCheckout, SubscriptionManager

@admin.register(SubscriptionCheckout)
class SubscriptionCheckoutAdmin(admin.ModelAdmin):
    list_display = ["checkout_id", "user", "plan", "used"]

@admin.register(SubscriptionManager)
class SubscriptionManagerAdmin(admin.ModelAdmin):
    list_display = ["manager_id", "user", "used"]
