from unittest.mock import MagicMock, patch, call
from django.test import TestCase
from authentication.models import User
from mails.models import UserMail
from core.celery import periodic_check_mails

class PeriodicCheckMailsTestCase(TestCase):
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
            name='Any Name',
            mail_user='any_user',
        )

    @patch('mails.tasks.listdir', MagicMock(return_value=['any-file']))
    @patch('mails.tasks.isfile', MagicMock(return_value=True))
    @patch('mails.tasks.save_user_late_mail.delay')
    def test_fetch_losed_mails(self, mock_delay: MagicMock):
        periodic_check_mails()

        path = "/home/%s/Mail/Inbox/new/any-file" % self.mail.mail_user

        mock_delay.assert_called_once_with(self.mail.pk, path)

    @patch('mails.tasks.listdir', MagicMock(return_value=['any-file']))
    @patch('mails.tasks.isfile', MagicMock(return_value=True))
    @patch('mails.tasks.save_user_late_mail.delay')
    def test_fetch_losed_mails_with_more_mails(self, mock_delay: MagicMock):
        mail2 = UserMail.objects.create(
            user=self.user,
            name='Any Name',
            mail_user='any_user2',
        )

        periodic_check_mails()

        path = "/home/%s/Mail/Inbox/new/any-file" % self.mail.mail_user
        path2 = "/home/%s/Mail/Inbox/new/any-file" % mail2.mail_user

        mock_delay.assert_has_calls([
            call(self.mail.pk, path),
            call(mail2.pk, path2),
        ])

        mail2.delete()

    @patch('mails.tasks.listdir', MagicMock(return_value=[]))
    @patch('mails.tasks.isfile', MagicMock(return_value=True))
    @patch('mails.tasks.save_user_late_mail.delay')
    def test_fetch_losed_mails_without_mails(self, mock_delay: MagicMock):
        periodic_check_mails()

        mock_delay.assert_not_called()
