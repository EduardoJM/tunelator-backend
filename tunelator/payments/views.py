from rest_framework import views, response
from django.conf import settings
from django.shortcuts import render, redirect
import stripe

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

    price_id = data["price_id"]
    session = stripe.checkout.Session.create(
        success_url='https://dashboard.tunelator.com.br/checkout/success',
        cancel_url='https://dashboard.tunelator.com.br/checkout/canceled',
        mode='subscription',
        line_items=[{
            'price': price_id,
            'quantity': 1
        }],
    )

    print(session)
    print(dir(session))

    return redirect(session.url, status=303)
