from django.urls import reverse
from rest_framework.test import APITestCase

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
