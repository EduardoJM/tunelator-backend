from unittest.mock import MagicMock, patch
from django.test import TestCase
from authentication.models import User
from mails.models import UserMail
from mails.tasks import (
    check_user_late_mails,
    save_user_late_mail
)

class CheckUserLateMailsTestCase(TestCase):
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
        check_user_late_mails(self.mail.pk)

        path = "/home/%s/Mail/Inbox/new/any-file" % self.mail.mail_user

        mock_delay.assert_called_once_with(self.mail.pk, path)

    @patch('mails.tasks.listdir', MagicMock(return_value=[]))
    @patch('mails.tasks.isfile', MagicMock(return_value=True))
    @patch('mails.tasks.save_user_late_mail.delay')
    def test_fetch_losed_mails_without_mails(self, mock_delay: MagicMock):
        check_user_late_mails(self.mail.pk)

        mock_delay.assert_not_called()

    @patch('mails.tasks.save_mail_from_file')
    @patch('mails.tasks.remove')
    def test_save_late_mails(self, mock_remove: MagicMock, mock_save: MagicMock):
        path = "/any-file"
        save_user_late_mail(self.mail.pk, path)

        mock_save.assert_called_once_with(self.mail, path)
        mock_remove.assert_called_once_with(path)

    def test_save_late_mails_without_valid_id(self):
        path = "/any-file"
        with self.assertRaises(Exception):
            save_user_late_mail(self.mail.pk + 50, path)
