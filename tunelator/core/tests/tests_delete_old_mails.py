from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from unittest import mock
from authentication.models import User
from mails.models import UserMail, UserReceivedMail
from core.celery import periodic_delete_old_mails

class CleanStripeCheckoutIdsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="example.123456@example.com"
        )
        self.mail = UserMail.objects.create(
            user=self.user,
            name='demo',
            mail_user='demo',
            mail='demo@demo.com'
        )

    def create_received_mail(self, date):
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=date)):
            mail = UserReceivedMail.objects.create(
                mail=self.mail,
                origin_mail='demo@demo.com',
                subject='demo',
                raw_mail='raw'
            )
        return mail

    def test_delete_mails_with_more_than_30_days(self):
        date = timezone.now() - timedelta(days=30, minutes=1)
        received = self.create_received_mail(date)
        id = received.pk

        periodic_delete_old_mails()

        self.assertIsNone(
            UserReceivedMail.objects.filter(pk=id).first()
        )

    def test_delete_mails_with_less_than_30_days(self):
        date = timezone.now() - timedelta(days=29, hours=23, minutes=58)
        received = self.create_received_mail(date)
        id = received.pk

        periodic_delete_old_mails()

        self.assertIsNotNone(
            UserReceivedMail.objects.filter(pk=id).first()
        )
