from rest_framework import views, response
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.middleware.csrf import get_token
from plans.models import Approval, Plan
from plans.plan import Plan as PlanIntegration
import stripe

User = get_user_model()

class DjangoGetCSRFTokenAPIView(views.APIView):
    def post(self, request):
        data = {
            'token': get_token(request)
        }
        return response.Response(data)

class StripeWebHookAPIView(views.APIView):
    permission_classes = []
    
    def post(self, request):
        data = request.data
        data_object = data["data"]["object"]
        event_type = data["type"]
        if event_type == "checkout.session.completed":
            checkout_id = data_object["id"]
            subscription_id = data_object["subscription"]
            customer_id = data_object["customer"]
            approval = Approval.objects.filter(stripe_session_id=checkout_id).first()
            if not approval:
                return response.Response()
            approval.stripe_subscription_id = subscription_id
            approval.stripe_customer_id = customer_id
            approval.save()
        elif event_type in ["customer.subscription.updated", "customer.subscription.deleted"]:
            subscription_id = data_object["id"]
            approval = Approval.objects.filter(stripe_subscription_id=subscription_id).first()
            if not approval:
                return response.Response()
            approval.status = data_object["status"]
            approval.save()
        return response.Response()

def test_stripe(request):
    return render(request, 'demo/go_to_checkout.html')

def stripe_subscription_manage_view(request):
    stripe.api_key = settings.STRIPE_ACCESS_TOKEN

    data = request.POST
    approval_id = data["approval_id"]
    approval = Approval.objects.filter(pk=approval_id).first()
    if not approval:
        return redirect('https://dashboard.tunelator.com.br/checkout/canceled', status=303)
    
    customer_id = approval.stripe_customer_id
    return_url = 'https://dashboard.tunelator.com.br'

    session = stripe.billing_portal.Session.create(
        customer=customer_id,
        return_url=return_url,
    )
    return redirect(session.url, status=303)

def stripe_subscription_view(request):
    stripe.api_key = settings.STRIPE_ACCESS_TOKEN

    data = request.POST

    user_id = data["user_id"]
    user = User.objects.filter(pk=user_id).first()
    if not user:
        return redirect('https://dashboard.tunelator.com.br/checkout/canceled', status=303)
    plan_util = PlanIntegration(user)
    if plan_util.is_paid_approval():
        return redirect('https://dashboard.tunelator.com.br/checkout/canceled', status=303)

    plan_id = data["plan_id"]
    plan = Plan.objects.filter(pk=plan_id).first()
    if not plan:
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
