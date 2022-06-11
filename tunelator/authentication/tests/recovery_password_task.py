from django.test import TestCase, override_settings
from django.core import mail
from authentication.models import User, ForgotPasswordSession
from authentication.tasks import send_recovery_link

class SendRecoveryLinkTestCase(TestCase):
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
    
    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_send_recovery_password_email(self):
        session = ForgotPasswordSession.objects.filter(user=self.user).first()
        self.assertIsNone(session)
        
        send_recovery_link(self.email)

        session = ForgotPasswordSession.objects.filter(user=self.user).first()
        self.assertIsNotNone(session)

        self.assertEqual(len(mail.outbox), 1)
        self.assertListEqual(mail.outbox[0].to, [self.email])
        
        mail.outbox.clear()

    def test_send_recovery_password_wrong_email(self):
        session = ForgotPasswordSession.objects.filter(user=self.user).first()
        self.assertIsNone(session)
        
        with self.assertRaises(Exception):
            send_recovery_link('another@example.com')

        session = ForgotPasswordSession.objects.filter(user=self.user).first()
        self.assertIsNone(session)

        self.assertEqual(len(mail.outbox), 0)
