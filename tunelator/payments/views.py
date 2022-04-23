from rest_framework import views, response
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
import stripe

from tunelator.plans.models import Approval, Plan

User = get_user_model()

class StripeWebHookAPIView(views.APIView):
    permission_classes = []
    
    def post(self, request):
        print(request.data)
        return response.Response()

def test_stripe(request):
    return render(request, 'demo/go_to_checkout.html')

def stripe_subscription_view(request):
    stripe.api_key = settings.STRIPE_ACCESS_TOKEN

    data = request.POST

    plan_id = data["plan_id"]
    plan = Plan.objects.filter(pk=plan_id).first()
    if not plan:
        return redirect('https://dashboard.tunelator.com.br/checkout/canceled', status=303)
    
    user_id = data["user_id"]
    user = User.objects.filter(pk=user_id).first()
    if not user:
        return redirect('https://dashboard.tunelator.com.br/checkout/canceled', status=303)

    session = stripe.checkout.Session.create(
        success_url='https://dashboard.tunelator.com.br/checkout/success',
        cancel_url='https://dashboard.tunelator.com.br/checkout/canceled',
        mode='subscription',
        line_items=[{
            'price': plan.stripe_price_id,
            'quantity': 1
        }],
    )

    Approval.objects.create(
        user=user,
        plan=plan,
        stripe_session_id=session.id,    
    )

    return redirect(session.url, status=303)
