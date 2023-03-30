from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model

class UserModelTest(TestCase):
    def setUp(self):
        self.user_email = "example@example.com"
        self.user_password = "password123"
        self.user = get_user_model().objects.create_user(
            email=self.user_email,
            password=self.user_password
        )

    def test_user_creation(self):
        self.assertTrue(isinstance(self.user, get_user_model()))
        self.assertEqual(self.user.__str__(), self.user.email)
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertEqual(self.user.date_joined.date(), timezone.now().date())
        self.assertEqual(self.user.email, self.user_email)

    def test_user_model_manager(self):
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(get_user_model().objects.create_user(
            email='example2@example.com',
            password=self.user_password
        ).email, 'example2@example.com')


