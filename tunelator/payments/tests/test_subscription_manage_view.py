from django.test import TestCase
from django.urls import reverse
from django.http import HttpResponseRedirect
from unittest.mock import MagicMock, Mock, patch
from authentication.models import User
from plans.models import Plan, Approval
from payments.models import SubscriptionManager
from payments.views import stripe_subscription_view

class StripeSubscriptionManageViewTestCase(TestCase):
    error_response = 'https://dashboard.tunelator.com.br/customer/error'
    return_url = 'https://dashboard.tunelator.com.br'

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
        url = reverse('manage-view', args=['uid-token'])
        response = self.client.get(url)

        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.error_response)

    def test_used_subscription(self):
        used_manager = SubscriptionManager.objects.create(
            user=self.user,
            used=True
        )

        url = reverse('manage-view', args=[used_manager.manager_id])
        response = self.client.get(url)

        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.error_response)
    
    def test_without_paid_approval(self):
        manager = SubscriptionManager.objects.create(user=self.user)

        url = reverse('manage-view', args=[manager.manager_id])
        response = self.client.get(url)

        manager = SubscriptionManager.objects.get(pk=manager.pk)

        self.assertTrue(manager.used)
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.error_response)

    @patch('payments.views.stripe.billing_portal.Session.create')
    def test_user_with_valid_checkout(self, mock_stripe: MagicMock):
        plan2 = Plan.objects.create(
            name=self.plan_name,
            description=self.plan_description,
            plan_type=Plan.TYPE_PAID
        )
        approval = Approval.objects.create(
            user=self.user,
            plan=plan2,
            stripe_session_id='session-id',
            stripe_subscription_id='subscription-id',
            stripe_customer_id='customer-id',
            status=Approval.STATUS_ACTIVE
        )
        manager = SubscriptionManager.objects.create(user=self.user)
        stripe_url = 'http://any_stripe_url.com/'

        mock_stripe.return_value = MagicMock()
        mock_stripe.return_value.url = stripe_url

        url = reverse('manage-view', args=[manager.manager_id])
        response = self.client.get(url)

        manager = SubscriptionManager.objects.get(pk=manager.pk)
        
        self.assertTrue(manager.used)
        
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, stripe_url)
        mock_stripe.assert_called_once_with(customer=approval.stripe_customer_id, return_url=self.return_url)
    