from django.urls import path
from payments.views import (
    StripeWebHookAPIView,
    CreateCheckoutAPIView,
    stripe_subscription_view,
    stripe_subscription_manage_view,
)

urlpatterns = [
    path('checkout/', CreateCheckoutAPIView.as_view()),
    path('checkout/go/<uuid>/', stripe_subscription_view),
    path('manage/', stripe_subscription_manage_view),
    path('webhook/', StripeWebHookAPIView.as_view()),
]
