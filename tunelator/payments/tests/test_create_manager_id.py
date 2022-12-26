from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from authentication.models import User
from plans.models import Plan
from payments.models import SubscriptionManager

class CreateManagerIdAPITestCase(APITestCase):
    url = reverse('create-manager-uid')

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
        self.access = str(AccessToken.for_user(self.user))
    

    def test_create_manager_view_without_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=None)

        response = self.client.post(self.url)

        data = response.json()
        self.assertEqual(401, response.status_code)
        self.assertTrue('detail' in data)

    def test_create_manager_view_with_valid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer %s" % self.access)

        response = self.client.post(self.url)

        data = response.json()
        self.assertEqual(200, response.status_code)
        self.assertTrue('manager_id' in data)
        
        manager_id = data.get("manager_id")
        manager = SubscriptionManager.objects.filter(manager_id=manager_id).first()
        
        self.assertIsNotNone(manager)
        self.assertEqual(manager.user.pk, self.user.pk)
