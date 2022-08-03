from django.test import TestCase
from django.contrib.auth import get_user_model

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