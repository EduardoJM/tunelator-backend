from django.urls import path
from payments.views import StripeWebHookAPIView, stripe_subscription_view, test_stripe

urlpatterns = [
    path('checkout/', stripe_subscription_view),
    path('test/', test_stripe),
    path('webhook/', StripeWebHookAPIView.as_view()),
]
