import json
from django.urls import reverse
from django.test import TestCase
from rest_framework_simplejwt.tokens import AccessToken
from unittest.mock import Mock, patch
from authentication.models import User
from mails.models import UserMail
from mails.tasks import create_mail_user
from exceptions.core import MailUserNotSentError, MailUserNotFoundError, InvalidMailUserIntegrationDataError

class CreateMailUserTaskAPITestCase(TestCase):
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
            name="Any Name Here",
            mail_user="example",
        )

    def test_without_mail_user_id(self):
        with self.assertRaises(MailUserNotSentError):
            create_mail_user(None)

    def test_with_invalid_mail_user_id(self):
        mail_user_id = 155545
        with self.assertRaises(MailUserNotFoundError):
            create_mail_user(mail_user_id)

    @patch('mails.tasks.requests.post')
    def test_with_wrong_request_status_code(self, mock_post):
        mock_post.return_value = Mock(ok=False)
        mock_post.return_value.status_code = 400
        mock_post.return_value.text = json.dumps({})

        with self.assertRaises(InvalidMailUserIntegrationDataError):
            create_mail_user(self.mail.pk)

    @patch('mails.tasks.requests.post')
    def test_with_wrong_request_response_data(self, mock_post):
        mock_post.return_value = Mock(ok=True)
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = json.dumps({})

        with self.assertRaises(InvalidMailUserIntegrationDataError):
            create_mail_user(self.mail.pk)
        
    @patch('mails.tasks.requests.post')
    def test_without_user_name(self, mock_post):
        mock_post.return_value = Mock(ok=True)
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = json.dumps({
            'data': {
            }
        })

        with self.assertRaises(InvalidMailUserIntegrationDataError):
            create_mail_user(self.mail.pk)

    @patch('mails.tasks.requests.post')
    def test_with_valid_return_data(self, mock_post):
        mail_user = "any_user_name"

        mock_post.return_value = Mock(ok=True)
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = json.dumps({
            'data': {
                'user_name': mail_user
            }
        })

        create_mail_user(self.mail.pk)

        mail = UserMail.objects.get(pk=self.mail.pk)
        
        self.assertEqual(mail.mail_user, mail_user)
        self.assertEqual(mail.mail, "%s@tunelator.com.br" % mail_user)
