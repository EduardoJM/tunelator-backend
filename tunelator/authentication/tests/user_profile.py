from django.urls import reverse
from rest_framework.test import APITestCase
from authentication.models import User
from rest_framework_simplejwt.tokens import AccessToken

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

    def test_update_user_password(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access)
        
        password = self.user.password
        send_password = 'any new password'

        response = self.client.patch(self.url, {
            'password': send_password,
        })

        user = User.objects.filter(pk=self.user.id).first()
        new_password = user.password

        self.assertEqual(200, response.status_code)
        self.assertNotEqual(password, new_password)
        self.assertNotEqual(new_password, send_password)
