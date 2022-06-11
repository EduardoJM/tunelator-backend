from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
from authentication.models import User, ForgotPasswordSession
from authentication.tasks import send_recovery_link
from unittest.mock import MagicMock

class ForgotPasswordSessionAPITestCase(APITestCase):
    url = reverse('authentication:recovery')

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

        self.mock = MagicMock()
        self.original_delay = send_recovery_link.delay
        send_recovery_link.delay = self.mock
    
    def tearDown(self):
        send_recovery_link.delay = self.original_delay

    def test_send_recovery_link_call_task(self):
        response = self.client.post(self.url, {
            'email': self.email,
        })

        self.assertEqual(200, response.status_code)
        self.mock.assert_called_once_with(self.email)

class ForgotPasswordValidateSessionAPITestCase(APITestCase):
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

        self.session = ForgotPasswordSession.objects.create(user=self.user)
        self.valid_url = reverse(
            'authentication:recovery-validate',
            args=[self.session.session_id]
        )
        self.invalid_url = reverse(
            'authentication:recovery-validate',
            args=['unk-session']
        )

    def test_validate_valid_forgot_password_session(self):
        self.session.valid_until = None
        self.session.used = False
        self.session.save()

        response = self.client.get(self.valid_url)

        self.assertEqual(200, response.status_code)

    def test_expired_forgot_password_session(self):
        self.session.valid_until = timezone.now()
        self.session.used = False
        self.session.save()

        response = self.client.get(self.valid_url)

        self.assertEqual(422, response.status_code)

    def test_used_forgot_password_session(self):
        self.session.used = True
        self.session.save()

        response = self.client.get(self.valid_url)

        self.assertEqual(422, response.status_code)

    def test_wrong_forgot_password_session(self):
        response = self.client.get(self.invalid_url)

        self.assertEqual(404, response.status_code)

class ForgotPasswordSessionResetAPITestCase(APITestCase):
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

        self.session = ForgotPasswordSession.objects.create(user=self.user)
        self.valid_url = reverse(
            'authentication:recovery-reset',
            args=[self.session.session_id]
        )
        self.invalid_url = reverse(
            'authentication:recovery-reset',
            args=['unk-session']
        )

    def test_validate_valid_forgot_password_session(self):
        self.session.valid_until = None
        self.session.used = False
        self.session.save()

        raw_password = self.user.password
        response = self.client.put(self.valid_url, {
            'password': 'any-password',
        })

        new_user = User.objects.filter(pk=self.user.pk).first()

        self.assertEqual(200, response.status_code)
        self.assertNotEqual(raw_password, new_user.password)

    def test_expired_forgot_password_session(self):
        self.session.valid_until = timezone.now()
        self.session.used = False
        self.session.save()

        raw_password = self.user.password
        response = self.client.put(self.valid_url, {
            'password': 'any-password'
        })

        new_user = User.objects.filter(pk=self.user.pk).first()

        self.assertEqual(422, response.status_code)
        self.assertEqual(raw_password, new_user.password)

    def test_used_forgot_password_session(self):
        self.session.used = True
        self.session.save()

        raw_password = self.user.password
        response = self.client.put(self.valid_url, {
            'password': 'any-password'
        })

        new_user = User.objects.filter(pk=self.user.pk).first()

        self.assertEqual(422, response.status_code)
        self.assertEqual(raw_password, new_user.password)

    def test_wrong_forgot_password_session(self):
        response = self.client.put(self.invalid_url)

        self.assertEqual(404, response.status_code)

