from django.urls import path
from payments.views import (
    DjangoGetCSRFTokenAPIView,
    StripeWebHookAPIView,
    CreateCheckoutAPIView,
    stripe_subscription_view,
    stripe_subscription_manage_view,
    test_stripe
)

urlpatterns = [
    path('token/', DjangoGetCSRFTokenAPIView.as_view()),
    path('checkout/', CreateCheckoutAPIView.as_view()),
    path('checkout/go/<uuid>/', stripe_subscription_view),
    path('manage/', stripe_subscription_manage_view),
    #path('test/', test_stripe),
    path('webhook/', StripeWebHookAPIView.as_view()),
]
