from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from unittest.mock import MagicMock
from authentication.models import User
from mails.models import UserMail
from mails.tasks import create_mail_user

class UserMailAPITestCase(APITestCase):
    def setUp(self):
        self.first_email = 'example@example.com.br'
        self.last_email = 'test@example.com'
        self.password = 'any password'
        self.first_name = 'First'
        self.last_name = 'Last'
        self.first_user = User.objects.create_user(
            email=self.first_email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name
        )
        self.second_user = User.objects.create_user(
            email=self.last_email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name
        )
        self.first_access = str(AccessToken.for_user(self.first_user))
        self.second_access = str(AccessToken.for_user(self.second_user))

        self.mock = MagicMock()
        self.original_delay = create_mail_user.apply_async
        create_mail_user.apply_async = self.mock

        self.first_mail_accounts = [
            UserMail.objects.create(
                user=self.first_user,
                name='Any Name',
                mail_user='any_user',
            ),
            UserMail.objects.create(
                user=self.first_user,
                name='Any Name 2',
                mail_user='any_user2',
            )
        ]
        self.second_mail_accounts = [
            UserMail.objects.create(
                user=self.second_user,
                name='Any Name 3',
                mail_user='any_user3',
            ),
        ]
    
    def tearDown(self):
        create_mail_user.apply_async = self.original_delay
    
    def test_list_user_emails_without_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=None)
        url = reverse('mails:UserMail-list')
        response = self.client.get(url)

        self.assertEqual(401, response.status_code)
        self.assertTrue("detail" in response.json())

    def test_list_user_emails_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.first_access)

        url = reverse('mails:UserMail-list')
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(200, response.status_code)
        self.assertEqual(data['count'], len(self.first_mail_accounts))
        self.assertEqual(data['next'], None)
        self.assertEqual(data['previous'], None)
        self.assertEqual(len(data['results']), len(self.first_mail_accounts))
        
        ids1 = sorted([result['id'] for result in data['results']])
        ids2 = sorted([result.pk for result in self.first_mail_accounts])
        self.assertListEqual(ids1, ids2)

    def test_list_other_user_emails_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.second_access)

        url = reverse('mails:UserMail-list')
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(200, response.status_code)
        self.assertEqual(data['count'], len(self.second_mail_accounts))
        self.assertEqual(data['next'], None)
        self.assertEqual(data['previous'], None)
        self.assertEqual(len(data['results']), len(self.second_mail_accounts))
        
        ids1 = sorted([result['id'] for result in data['results']])
        ids2 = sorted([result.pk for result in self.second_mail_accounts])
        self.assertListEqual(ids1, ids2)

    def test_paginated_list_user_emails_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.second_access)

        new_accounts = []
        for i in range(0, 11):
            new_accounts += [
                UserMail.objects.create(
                    user=self.second_user,
                    name='New Account %s' % i,
                    mail_user='any_user_new_%s' % i,
                ),
            ]
        
        result_accounts = [*new_accounts, *self.second_mail_accounts]

        url = reverse('mails:UserMail-list')
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(200, response.status_code)
        self.assertEqual(data['count'], len(result_accounts))
        self.assertIsNotNone(data['next'], None)
        self.assertEqual(data['previous'], None)
        self.assertEqual(len(data['results']), 10)

        for item in new_accounts:
            item.delete()

    def test_create_mail_account(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.first_access)
        self.mock = MagicMock()
        create_mail_user.apply_async = self.mock

        name = "Creating an Account"
        mail_user = "creating_an_account"

        url = reverse('mails:UserMail-list')
        response = self.client.post(url, {
            "name": name,
            "mail_user": mail_user,
        })

        account = UserMail.objects.filter(name=name).first()

        self.assertEqual(201, response.status_code)
        self.assertIsNotNone(account)
        self.mock.assert_called_once_with(args=[account.pk], countdown=2)
