from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from authentication.models import User
from mails.models import UserMail
from plans.models import Approval, Plan, PlanConfigurationIntegerItem

class ActivePlanAPITestCase(APITestCase):
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
        
        self.mails = 4
        self.plan_mails = PlanConfigurationIntegerItem.objects.create(
            plan=self.plan,
            name='mails',
            value=self.mails
        )

        self.url = reverse('plans:Plan-active')
        
    def test_get_active_plan(self):
        approval = Approval.objects.create(
            user=self.user,
            plan=self.plan,
            status=Approval.STATUS_ACTIVE
        )

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access)

        response = self.client.get(self.url)

        data = response.json()

        self.assertEqual(200, response.status_code)
        self.assertEqual(data['id'], self.plan.pk)
        self.assertEqual(data['name'], self.plan_name)
        self.assertEqual(data['description'], self.plan_description)
        self.assertEqual(data['free_accounts'], self.mails)

        approval.delete()

    def test_get_active_plan_reduce_free_accounts(self):
        approval = Approval.objects.create(
            user=self.user,
            plan=self.plan,
            status=Approval.STATUS_ACTIVE
        )
        account1 = UserMail.objects.create(
            user=self.user,
            name='any-name',
            mail_user='any_any',
        )
        account2 = UserMail.objects.create(
            user=self.user,
            name='any-name',
            mail_user='any_any',
        )

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access)

        response = self.client.get(self.url)

        data = response.json()

        self.assertEqual(200, response.status_code)
        self.assertEqual(data['id'], self.plan.pk)
        self.assertEqual(data['name'], self.plan_name)
        self.assertEqual(data['description'], self.plan_description)
        self.assertEqual(data['free_accounts'], self.mails - 2)

        account1.delete()
        account2.delete()
        approval.delete()

    def test_get_active_plan_without_authorization(self):
        self.client.credentials(HTTP_AUTHORIZATION=None)

        response = self.client.get(self.url)

        data = response.json()
        self.assertEqual(401, response.status_code)
        self.assertTrue('detail' in data)

    def test_get_active_plan_without_approval(self):
        self.plan.plan_type = Plan.TYPE_FREE
        self.plan.save()
        self.assertIsNone(Approval.objects.filter(user=self.user).first())

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access)

        response = self.client.get(self.url)

        data = response.json()

        self.assertEqual(200, response.status_code)
        self.assertEqual(data['id'], self.plan.pk)
        self.assertEqual(data['name'], self.plan_name)
        self.assertEqual(data['description'], self.plan_description)
        self.assertEqual(data['free_accounts'], self.mails)

        self.assertIsNotNone(Approval.objects.filter(user=self.user).first())
        self.assertEqual(Approval.objects.filter(user=self.user).first().plan.pk, self.plan.pk)

        self.plan.plan_type = Plan.TYPE_PAID
        self.plan.save()
