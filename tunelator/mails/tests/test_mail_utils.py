import os
from django.conf import settings
from django.test import TestCase, override_settings
from django.core import mail
from unittest.mock import MagicMock, Mock, patch
from authentication.models import User
from mails.models import UserMail, UserReceivedMail
from mails import utils
from mails.tasks import send_redirect_mail

class TestMailUtilsTestCase(TestCase):
    def read_file(self, path: str):
        dir = os.path.dirname(__file__)
        full_path = os.path.join(dir, 'files', path)
        with open(full_path, 'r') as f:
            text = '\n'.join(f.readlines())
        return text

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
        self.mail = UserMail.objects.create(
            user=self.user,
            name='any-name',
            mail_user='any-name',
            mail='any-mail'
        )

        self.problematic_received_mails = [
            UserReceivedMail.objects.create(
                mail=self.mail,
                raw_mail=self.read_file('twilo.txt')
            ),
            UserReceivedMail.objects.create(
                mail=self.mail,
                raw_mail=self.read_file('canva.txt')
            )
        ]
    
    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    @patch('mails.tasks.send_email')
    def test_problematic_received_mails(self, mock: MagicMock):
        for mail in self.problematic_received_mails:
            send_redirect_mail(mail.pk, True)
            
            mock.assert_called_once()
            
            mail_msg = str(mock.call_args[0][1])
            self.assertTrue('tunelator.com.br' in mail_msg)

            mock.reset_mock()
