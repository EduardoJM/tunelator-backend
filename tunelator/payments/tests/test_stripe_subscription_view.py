from django.test import TestCase
from django.urls import reverse
from django.http import HttpResponseRedirect
from unittest.mock import MagicMock, Mock, patch
from authentication.models import User
from plans.models import Plan, Approval
from payments.models import SubscriptionCheckout
from payments.views import stripe_subscription_view

class StripeSubscriptionViewTestCase(TestCase):
    error_response = 'https://dashboard.tunelator.com.br/checkout/error'
    already_paid = 'https://dashboard.tunelator.com.br/checkout/already-paid'

    def setUp(self):
        self.email = 'example@example.com.br'
        self.password = 'any password'
        self.first_name = 'First'
        self.last_name = 'Last'
        self.user = User.objects.create_user(
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name
        )

        self.plan_name = 'Any Name of Plan'
        self.plan_description = 'Any Plan Description'
        self.plan = Plan.objects.create(
            name=self.plan_name,
            description=self.plan_description,
            plan_type=Plan.TYPE_FREE
        )

    def test_not_subscription_found(self):
        url = reverse('checkout-view', args=['uid-token'])
        response = self.client.get(url)

        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.error_response)

    def test_used_subscription(self):
        used_checkout = SubscriptionCheckout.objects.create(
            user=self.user,
            plan=self.plan,
            used=True
        )

        url = reverse('checkout-view', args=[used_checkout.checkout_id])
        response = self.client.get(url)

        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.error_response)

    def test_user_with_paid_approval(self):
        self.plan2 = Plan.objects.create(
            name=self.plan_name,
            description=self.plan_description,
            plan_type=Plan.TYPE_PAID
        )
        self.approval = Approval.objects.create(
            plan=self.plan2,
            user=self.user,
            stripe_session_id='any',
            stripe_subscription_id='any',
            stripe_customer_id='any',
            status=Approval.STATUS_ACTIVE
        )
        checkout = SubscriptionCheckout.objects.create(
            user=self.user,
            plan=self.plan,
        )

        url = reverse('checkout-view', args=[checkout.checkout_id])
        response = self.client.get(url)

        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.already_paid)
    
    @patch('payments.views.stripe.checkout.Session.create')
    def test_user_with_valid_checkout(self, mock_stripe: MagicMock):
        plan2 = Plan.objects.create(
            name=self.plan_name,
            description=self.plan_description,
            plan_type=Plan.TYPE_PAID
        )
        checkout = SubscriptionCheckout.objects.create(
            user=self.user,
            plan=plan2,
        )
        stripe_id = 'any-stripe-id'
        stripe_url = 'http://any_stripe_url.com/'

        mock_stripe.return_value = MagicMock()
        mock_stripe.return_value.id = stripe_id
        mock_stripe.return_value.url = stripe_url

        url = reverse('checkout-view', args=[checkout.checkout_id])
        response = self.client.get(url)

        checkout = SubscriptionCheckout.objects.get(pk=checkout.pk)
        approval = Approval.objects.filter(user=self.user, plan=plan2).first()
        
        self.assertTrue(checkout.used)
        self.assertIsNotNone(approval)
        self.assertEqual(approval.stripe_session_id, stripe_id)

        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, stripe_url)
