from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from authentication.models import User
from plans.models import Plan
from payments.models import SubscriptionCheckout

class CreateCheckoutIdAPITestCase(APITestCase):
    url = reverse('create-checkout-uid')

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
        
        self.plan_name = 'Any Name of Plan'
        self.plan_description = 'Any Plan Description'
        self.plan = Plan.objects.create(
            name=self.plan_name,
            description=self.plan_description,
        )

    def test_create_checkout_view_without_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=None)

        response = self.client.post(self.url)

        data = response.json()
        self.assertEqual(401, response.status_code)
        self.assertTrue('detail' in data)

    def test_create_checkout_view_without_plan_data(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer %s" % self.access)

        response = self.client.post(self.url, data={})

        data = response.json()
        self.assertEqual(400, response.status_code)
        self.assertTrue('plan' in data)

    def test_create_checkout_view_with_valid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer %s" % self.access)

        response = self.client.post(self.url, data={
            'plan': self.plan.pk,
        })

        data = response.json()
        self.assertEqual(200, response.status_code)
        self.assertTrue('checkout_id' in data)
        
        checkout_id = data.get("checkout_id")
        checkout = SubscriptionCheckout.objects.filter(checkout_id=checkout_id).first()
        
        self.assertIsNotNone(checkout)
        self.assertEqual(checkout.user.pk, self.user.pk)
