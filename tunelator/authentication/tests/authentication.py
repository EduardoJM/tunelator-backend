from django.urls import reverse
from rest_framework.test import APITestCase
from authentication.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class TokenObtainPairViewAPITestCase(APITestCase):
    url = reverse('authentication:login')

    def setUp(self) -> None:
        self.email = 'example@example.com.br'
        self.password = 'any password'
        self.user = User.objects.create_user(email=self.email, password=self.password)
    
    def test_authentication_without_email(self):
        response = self.client.post(self.url, { 'password': self.password })
        
        data = response.json()
        
        self.assertEqual(400, response.status_code)
        self.assertTrue('email' in data)
    
    def test_authentication_without_password(self):
        response = self.client.post(self.url, { 'email': self.email })
        
        data = response.json()
                
        self.assertEqual(400, response.status_code)
        self.assertTrue('password' in data)
    
    def test_authentication_without_email_and_password(self):
        response = self.client.post(self.url, {})
        
        data = response.json()
        
        self.assertEqual(400, response.status_code)
        self.assertTrue('email' in data)
        self.assertTrue('password' in data)

    def test_authentication_with_wrong_password(self):
        response = self.client.post(self.url, { 'email': self.email, 'password': 'any wrong' })

        data = response.json()

        self.assertEqual(401, response.status_code)
        self.assertTrue('detail' in data)
    
    def test_authentication_with_valid_data(self):
        response = self.client.post(self.url, { 'email': self.email, 'password': self.password })

        data = response.json()
        
        self.assertEqual(200, response.status_code)
        self.assertTrue('access' in data)
        self.assertTrue('refresh' in data)
        self.assertTrue('user' in data)
        self.assertEqual(self.user.id, data['user']['id'])

    def test_authentication_should_update_last_login(self):
        response = self.client.post(self.url, { 'email': self.email, 'password': self.password })
        user = User.objects.filter(pk=self.user.pk).first()
        last_login = user.last_login

        data = response.json()
        
        self.assertTrue('user' in data)
        
        user = User.objects.filter(pk=self.user.pk).first()
        updated_last_login = user.last_login
        
        self.assertNotEqual(last_login, updated_last_login)

class TokenRefreshViewAPITestCase(APITestCase):
    url = reverse('authentication:refresh')

    def setUp(self) -> None:
        self.email = 'example@example.com.br'
        self.password = 'any password'
        self.user = User.objects.create_user(email=self.email, password=self.password)

        self.refresh = str(RefreshToken.for_user(self.user))

    def test_with_invalid_refresh_token(self):
        response = self.client.post(self.url, { 'refresh': 'invalid-token' })

        data = response.json()

        self.assertEqual(401, response.status_code)
        self.assertTrue('detail' in data)

    def test_with_valid_refresh_token(self):
        response = self.client.post(self.url, { 'refresh': self.refresh })

        data = response.json()

        self.assertEqual(200, response.status_code)
        self.assertTrue('access' in data)
        self.assertTrue('user' in data)
        self.assertEqual(self.user.id, data['user']['id'])
