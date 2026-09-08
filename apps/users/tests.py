from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(
            email="test@test.com",
            username="testuser",
            password="testpass123"
        )
        self.assertEqual(user.email, "test@test.com")
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("testpass123"))
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            email="admin@test.com",
            username="admin",
            password="adminpass123"
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_user_str(self):
        user = User.objects.create_user(
            email="str@test.com",
            username="struser",
            password="testpass123"
        )
        self.assertEqual(str(user), "str@test.com")

    def test_email_unique(self):
        User.objects.create_user(
            email="dup@test.com",
            username="user1",
            password="testpass123"
        )
        with self.assertRaises(Exception):
            User.objects.create_user(
                email="dup@test.com",
                username="user2",
                password="testpass123"
            )
