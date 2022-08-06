import datetime
from django.test import TestCase
from django.utils import timezone
from authentication.models import User, ForgotPasswordSession
from core.celery import periodic_clean_expired_forgot_password_sessions

class CleanExpiredForgotPasswordSessionsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="example.123456@example.com"
        )
    
    def test_clean_withtout_expired_and_no_used(self):
        session = ForgotPasswordSession.objects.create(
            user=self.user,
        )
        id = session.pk

        periodic_clean_expired_forgot_password_sessions()

        session = ForgotPasswordSession.objects.filter(pk=id).first()
        self.assertIsNotNone(session)
        session.delete()

    def test_clean_used(self):
        session = ForgotPasswordSession.objects.create(
            user=self.user,
            used=True
        )
        id = session.pk

        periodic_clean_expired_forgot_password_sessions()

        session = ForgotPasswordSession.objects.filter(pk=id).first()
        self.assertIsNone(session)

    def test_clean_expired(self):
        session = ForgotPasswordSession.objects.create(
            user=self.user,
        )
        time = timezone.now() - datetime.timedelta(minutes=1)
        session.valid_until = time
        session.save()
        id = session.pk

        periodic_clean_expired_forgot_password_sessions()

        session = ForgotPasswordSession.objects.filter(pk=id).first()
        self.assertIsNone(session)
