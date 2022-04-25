from django.urls import path
from payments.views import (
    StripeWebHookAPIView,
    CreateCheckoutAPIView,
    CreateManagerAPIView,
    stripe_subscription_view,
    stripe_subscription_manage_view,
)

urlpatterns = [
    path('checkout/', CreateCheckoutAPIView.as_view()),
    path('checkout/go/<uuid>/', stripe_subscription_view),
    path('manage/', CreateManagerAPIView.as_view()),
    path('manage/go/<uuid>/', stripe_subscription_manage_view),
    path('webhook/', StripeWebHookAPIView.as_view()),
]
