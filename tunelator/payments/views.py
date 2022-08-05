from rest_framework import views, response, status
from drf_yasg.utils import swagger_auto_schema
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
import stripe
from plans.models import Approval
from plans.plan import Plan as PlanIntegration
from payments.models import SubscriptionCheckout, SubscriptionManager
from payments.serializers import (
    SubscriptionCheckoutSerializer,
    SubscriptionCheckoutRetrieveSerializer,
    SubscriptionManagerSerializer,
    SubscriptionManagerRetrieveSerializer,
    # documentation only
    WebhookWaitedFieldsSerializer,
)
from docs.responses import UnauthenticatedResponse

User = get_user_model()

class CreateCheckoutAPIView(views.APIView):
    @swagger_auto_schema(
        request_body=SubscriptionCheckoutSerializer,
        responses={
            status.HTTP_200_OK: SubscriptionCheckoutRetrieveSerializer,
            status.HTTP_401_UNAUTHORIZED: UnauthenticatedResponse,
        }
    )
    def post(self, request):
        """
        Generates an unique checkout session id used to redirect user
        to the stripe payment page.
        """
        serializer = SubscriptionCheckoutSerializer(data=request.data, context={ 'request': request })
        serializer.is_valid(raise_exception=True)

        instance = serializer.save()
        
        serializer = SubscriptionCheckoutRetrieveSerializer(instance=instance)
        return response.Response(serializer.data)

class CreateManagerAPIView(views.APIView):
    @swagger_auto_schema(
        request_body=None,
        responses={
            status.HTTP_200_OK: SubscriptionManagerRetrieveSerializer,
            status.HTTP_401_UNAUTHORIZED: UnauthenticatedResponse,
        }
    )
    def post(self, request):
        """
        Generates an unique subscription manager session id used to
        redirect user to the subscription manager page on stripe
        payment system.
        """
        serializer = SubscriptionManagerSerializer(data={}, context={ 'request': request })
        serializer.is_valid(raise_exception=True)

        instance = serializer.save()
        
        serializer = SubscriptionManagerRetrieveSerializer(instance=instance)
        return response.Response(serializer.data)

class StripeWebHookAPIView(views.APIView):
    permission_classes = []
    
    @swagger_auto_schema(
        request_body=WebhookWaitedFieldsSerializer,
        responses={
            status.HTTP_200_OK: "No body",
        },
    )
    def post(self, request):
        """
        Webhook to receive status update and some data from the stripe
        payment system integration. You can see more about the stripe
        webhooks in the stripe documentations.
        """
        request_data = request.data
        data = request_data['data']
        event_type = request_data['type']
        data_object = data['object']
        
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

@csrf_exempt
def stripe_subscription_manage_view(request, uuid):
    stripe.api_key = settings.STRIPE_ACCESS_TOKEN

    manager = SubscriptionManager.objects.filter(
        manager_id=uuid
    ).first()
    
    if not manager or manager.used:
        return redirect('https://dashboard.tunelator.com.br/customer/error', status=303)
    
    manager.used = True
    manager.save()
    
    user = manager.user
    plan_util = PlanIntegration(user)
    if not plan_util.is_paid_approval():
        return redirect('https://dashboard.tunelator.com.br/customer/error', status=303)
    
    approval = plan_util.approval
    customer_id = approval.stripe_customer_id
    return_url = 'https://dashboard.tunelator.com.br'

    session = stripe.billing_portal.Session.create(
        customer=customer_id,
        return_url=return_url,
    )
    return redirect(session.url, status=303)

@csrf_exempt
def stripe_subscription_view(request, uuid):
    stripe.api_key = settings.STRIPE_ACCESS_TOKEN

    checkout = SubscriptionCheckout.objects.filter(
        checkout_id=uuid
    ).first()
    if not checkout or checkout.used:
        return redirect('https://dashboard.tunelator.com.br/checkout/error', status=303)

    user = checkout.user
    plan = checkout.plan

    plan_util = PlanIntegration(user)
    if plan_util.is_paid_approval():
        return redirect('https://dashboard.tunelator.com.br/checkout/already-paid', status=303)

    checkout.used = True
    checkout.save()

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
