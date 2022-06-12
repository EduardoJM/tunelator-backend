import datetime
from django.test import TestCase
from django.utils import timezone
from authentication.models import User
from core.celery import periodic_clean_stripe_checkout_ids
from payments.models import SubscriptionCheckout, SubscriptionManager
from plans.models import Plan

class CleanStripeCheckoutIdsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="example.123456@example.com"
        )
        self.plan = Plan.objects.create(
            name="My Plan",
            description="My Plan"
        )

    def create_checkout_with_timedelta(self, minutes = None):
        checkout = SubscriptionCheckout.objects.create(
            user=self.user,
            plan=self.plan,
            used=False,
        )
        if minutes is not None:
            checkout.created_at = timezone.now()
            checkout.created_at -= datetime.timedelta(minutes=minutes)
            checkout.save()
        return checkout

    def create_manager_with_timedelta(self, minutes = None):
        manager = SubscriptionManager.objects.create(
            user=self.user,
            used=False,
        )
        if minutes is not None:
            manager.created_at = timezone.now()
            manager.created_at -= datetime.timedelta(minutes=minutes)
            manager.save()
        return manager

    def test_remove_subscription_checkout_with_more_than_six_hours(self):
        six_hours_plus_one_minute = 6*60+1
        checkout = self.create_checkout_with_timedelta(six_hours_plus_one_minute)
        session_id = checkout.pk

        periodic_clean_stripe_checkout_ids()

        subscription = SubscriptionCheckout.objects.filter(pk=session_id).first()
        self.assertIsNone(subscription)

    def test_remove_subscription_checkout_with_exctly_six_hours(self):
        six_hours = 6*60
        checkout = self.create_checkout_with_timedelta(six_hours)
        session_id = checkout.pk

        periodic_clean_stripe_checkout_ids()

        subscription = SubscriptionCheckout.objects.filter(pk=session_id).first()
        self.assertIsNone(subscription)
    
    def test_remove_subscription_checkout_with_less_than_six_hours(self):
        six_hours_minus_one_minute = 5*60 + 59
        checkout = self.create_checkout_with_timedelta(six_hours_minus_one_minute)
        session_id = checkout.pk

        periodic_clean_stripe_checkout_ids()

        subscription = SubscriptionCheckout.objects.filter(pk=session_id).first()
        self.assertIsNotNone(subscription)

    def test_remove_subscription_checkout_with_used_true(self):
        checkout = self.create_checkout_with_timedelta()
        checkout.used = True
        checkout.save()
        session_id = checkout.pk

        periodic_clean_stripe_checkout_ids()

        subscription = SubscriptionCheckout.objects.filter(pk=session_id).first()
        self.assertIsNone(subscription)

    def test_remove_subscription_manager_with_more_than_six_hours(self):
        six_hours_plus_one_minute = 6*60+1
        manager = self.create_manager_with_timedelta(six_hours_plus_one_minute)
        session_id = manager.pk

        periodic_clean_stripe_checkout_ids()

        subscription = SubscriptionManager.objects.filter(pk=session_id).first()
        self.assertIsNone(subscription)

    def test_remove_subscription_manager_with_exctly_six_hours(self):
        six_hours = 6*60
        manager = self.create_manager_with_timedelta(six_hours)
        session_id = manager.pk

        periodic_clean_stripe_checkout_ids()

        subscription = SubscriptionManager.objects.filter(pk=session_id).first()
        self.assertIsNone(subscription)
    
    def test_remove_subscription_manager_with_less_than_six_hours(self):
        six_hours_minus_one_minute = 5*60 + 59
        manager = self.create_manager_with_timedelta(six_hours_minus_one_minute)
        session_id = manager.pk

        periodic_clean_stripe_checkout_ids()

        subscription = SubscriptionManager.objects.filter(pk=session_id).first()
        self.assertIsNotNone(subscription)

    def test_remove_subscription_manager_with_used_true(self):
        manager = self.create_manager_with_timedelta()
        manager.used = True
        manager.save()
        session_id = manager.pk

        periodic_clean_stripe_checkout_ids()

        subscription = SubscriptionManager.objects.filter(pk=session_id).first()
        self.assertIsNone(subscription)
