from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from .views import SignupView

class CustomUserTests(TestCase):

    def test_user_creation(self):
        user = get_user_model().objects.create_user(
            username="testuser01",
            email="testuser01@example.com",
            password="testpassword123"
        )

        self.assertEqual(user.username, "testuser01")
        self.assertEqual(user.email, "testuser01@example.com")
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

    def test_super_user_creation(self):
        super_user = get_user_model().objects.create_superuser(
            username="testsuperuser01",
            email="testsuperuser01@example.com",
            password="testsuperpassword123"
        )

        self.assertEqual(super_user.username, "testsuperuser01")
        self.assertEqual(super_user.email, "testsuperuser01@example.com")
        self.assertTrue(super_user.is_active)
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)

class SignupTests(TestCase):

    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertTemplateUsed(self.response, 'signup.html')

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_resolve_url(self):
        view = resolve('/accounts/signup/')
        self.assertEqual(view.func.view_class, SignupView)