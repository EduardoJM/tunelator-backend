from django.urls import reverse
from rest_framework.test import APITestCase
from authentication.models import User
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

class UserCreateViewAPITestCase(APITestCase):
    url = reverse('authentication:signup')

    def test_user_registration(self):
        email = 'example@example.com.br'
        user_data = {
            'email': email,
            'first_name': 'First',
            'last_name': 'Last',
            'password': 'any password',
        }
        response = self.client.post(self.url, user_data)

        data = response.json()

        self.assertEqual(201, response.status_code)
        self.assertTrue('access' in data)
        self.assertTrue('refresh' in data)
        self.assertTrue('user' in data)
        self.assertEqual(email, data['user']['email'])
    
    def test_without_valid_email(self):
        user_data = {
            'email': 'not-an-email',
            'first_name': 'First',
            'last_name': 'Last',
            'password': 'any password',
        }
        response = self.client.post(self.url, user_data)

        data = response.json()

        self.assertEqual(400, response.status_code)
        self.assertTrue('email' in data)
    
    def test_with_empty_email(self):
        user_data = {
            'email': '',
            'first_name': 'First',
            'last_name': 'Last',
            'password': 'any password',
        }
        response = self.client.post(self.url, user_data)

        data = response.json()

        self.assertEqual(400, response.status_code)
        self.assertTrue('email' in data)
    
    def test_without_email(self):
        user_data = {
            'first_name': 'First',
            'last_name': 'Last',
            'password': 'any password',
        }
        response = self.client.post(self.url, user_data)

        data = response.json()

        self.assertEqual(400, response.status_code)
        self.assertTrue('email' in data)

    def test_with_empty_first_name(self):
        user_data = {
            'email': 'example@example.com',
            'first_name': '',
            'last_name': 'Last',
            'password': 'any password',
        }
        response = self.client.post(self.url, user_data)

        data = response.json()

        self.assertEqual(400, response.status_code)
        self.assertTrue('first_name' in data)
    
    def test_without_first_name(self):
        user_data = {
            'email': 'example@example.com',
            'last_name': 'Last',
            'password': 'any password',
        }
        response = self.client.post(self.url, user_data)

        data = response.json()

        self.assertEqual(400, response.status_code)
        self.assertTrue('first_name' in data)
    
    def test_with_empty_last_name(self):
        user_data = {
            'email': 'example@example.com',
            'first_name': 'First',
            'last_name': '',
            'password': 'any password',
        }
        response = self.client.post(self.url, user_data)

        data = response.json()

        self.assertEqual(400, response.status_code)
        self.assertTrue('last_name' in data)
    
    def test_without_last_name(self):
        user_data = {
            'email': 'example@example.com',
            'first_name': 'First',
            'password': 'any password',
        }
        response = self.client.post(self.url, user_data)

        data = response.json()

        self.assertEqual(400, response.status_code)
        self.assertTrue('last_name' in data)
    
    def test_with_empty_password(self):
        user_data = {
            'email': 'example@example.com',
            'first_name': 'First',
            'last_name': 'Last',
            'password': '',
        }
        response = self.client.post(self.url, user_data)

        data = response.json()

        self.assertEqual(400, response.status_code)
        self.assertTrue('password' in data)
    
    def test_without_password(self):
        user_data = {
            'email': 'example@example.com',
            'first_name': 'First',
            'last_name': 'Last',
        }
        response = self.client.post(self.url, user_data)

        data = response.json()

        self.assertEqual(400, response.status_code)
        self.assertTrue('password' in data)
    
    def test_unique_email_validator(self):
        user_data = {
            'email': 'example12@example.com',
            'first_name': 'First',
            'last_name': 'Last',
            'password': '123456',
        }
        self.client.post(self.url, user_data)
        
        response = self.client.post(self.url, user_data)

        data = response.json()

        self.assertEqual(400, response.status_code)
        self.assertTrue('email' in data)

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

class UserProfileDataViewAPITestCase(APITestCase):
    url = reverse('authentication:user')

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

    def test_retrieve_data_without_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=None)
        response = self.client.get(self.url)

        data = response.json()

        self.assertEqual(401, response.status_code)
        self.assertTrue('detail' in data)
    
    def test_retrieve_user_data(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access)

        response = self.client.get(self.url)

        data = response.json()

        self.assertEqual(200, response.status_code)
        self.assertTrue('id' in data)
        self.assertTrue('email' in data)
        self.assertTrue('first_name' in data)
        self.assertTrue('last_name' in data)
        self.assertEqual(self.user.id, data['id'])
        self.assertEqual(self.email, data['email'])
        self.assertEqual(self.first_name, data['first_name'])
        self.assertEqual(self.last_name, data['last_name'])

    def test_update_user_without_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=None)
        response = self.client.patch(self.url, {})

        data = response.json()

        self.assertEqual(401, response.status_code)
        self.assertTrue('detail' in data)
    
    def test_update_user_first_name(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access)
        
        first_name = 'Another'
        response = self.client.patch(self.url, {
            'first_name': first_name
        })
        data = response.json()
        
        user = User.objects.filter(pk=self.user.id).first()

        self.assertEqual(200, response.status_code)
        self.assertTrue('id' in data)
        self.assertTrue('email' in data)
        self.assertTrue('first_name' in data)
        self.assertTrue('last_name' in data)
        self.assertEqual(self.user.id, data['id'])
        self.assertEqual(self.email, data['email'])
        self.assertEqual(first_name, data['first_name'])
        self.assertEqual(first_name, user.first_name)
        self.assertEqual(self.last_name, data['last_name'])
    
    def test_update_user_last_name(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access)
        
        last_name = 'Another'
        response = self.client.patch(self.url, {
            'last_name': last_name,
        })
        data = response.json()
        
        user = User.objects.filter(pk=self.user.id).first()

        self.assertEqual(200, response.status_code)
        self.assertTrue('id' in data)
        self.assertTrue('email' in data)
        self.assertTrue('first_name' in data)
        self.assertTrue('last_name' in data)
        self.assertEqual(self.user.id, data['id'])
        self.assertEqual(self.email, data['email'])
        self.assertEqual(last_name, data['last_name'])
        self.assertEqual(last_name, user.last_name)
        self.assertEqual(self.first_name, data['first_name'])
