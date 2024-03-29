from django.urls import path
from payments.views import (
    StripeWebHookAPIView,
    CreateCheckoutAPIView,
    CreateManagerAPIView,
    stripe_subscription_view,
    stripe_subscription_manage_view,
)

urlpatterns = [
    path('checkout/', CreateCheckoutAPIView.as_view(), name="create-checkout-uid"),
    path('checkout/go/<uuid>/', stripe_subscription_view, name='checkout-view'),
    path('manage/', CreateManagerAPIView.as_view(), name='create-manager-uid'),
    path('manage/go/<uuid>/', stripe_subscription_manage_view, name="manage-view"),
    path('webhook/', StripeWebHookAPIView.as_view()),
]
