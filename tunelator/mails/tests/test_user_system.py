from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from unittest.mock import Mock, patch
from authentication.models import User

class VerifyUserSystemAPITestCase(APITestCase):
    url = reverse('mails:verify_mail_user_name')

    def setUp(self) -> None:
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
        self.access = str(AccessToken.for_user(self.user))

    def test_verify_with_unauthenticated_account(self):
        self.client.credentials(HTTP_AUTHORIZATION=None)

        response = self.client.post(self.url, {
            'user_name': 'any_user_name'
        })

        self.assertEqual(401, response.status_code)
        self.assertTrue('detail' in response.json())
    
    @patch('mails.services.requests.post')
    def test_verify_free_user_account_name(self, mock_post):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access)

        mock_post.return_value = Mock(ok=True)
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {}

        response = self.client.post(self.url, {
            'user_name': 'test'
        })
        self.assertEqual(200, response.status_code)
        self.assertTrue('detail' in response.json())
    
    @patch('mails.services.requests.post')
    def test_verify_used_user_account_name(self, mock_post):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access)

        mock_post.return_value = Mock(ok=True)
        mock_post.return_value.status_code = 400
        mock_post.return_value.json.return_value = {}

        response = self.client.post(self.url, {
            'user_name': 'test'
        })
        self.assertEqual(400, response.status_code)
        self.assertTrue('detail' in response.json())
