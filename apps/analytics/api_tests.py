from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class RegisterEndpointTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.register_url = "/api/auth/register/"
        self.valid_data = {
            "email": "new@test.com",
            "username": "newuser",
            "password": "testpass123"
        }

    def test_register_success(self):
        response = self.client.post(
            self.register_url,
            self.valid_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="new@test.com").exists())

    def test_register_duplicate_email(self):
        User.objects.create_user(
            email="dup@test.com",
            username="user1",
            password="testpass123"
        )
        response = self.client.post(
            self.register_url,
            {"email": "dup@test.com", "username": "user2", "password": "testpass123"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_missing_fields(self):
        response = self.client.post(
            self.register_url,
            {"email": "inc@test.com"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginEndpointTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.login_url = "/api/auth/login/"
        self.user = User.objects.create_user(
            email="login@test.com",
            username="loginuser",
            password="testpass123"
        )

    def test_login_success(self):
        response = self.client.post(
            self.login_url,
            {"email": "login@test.com", "password": "testpass123"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_wrong_password(self):
        response = self.client.post(
            self.login_url,
            {"email": "login@test.com", "password": "wrongpass"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_nonexistent_user(self):
        response = self.client.post(
            self.login_url,
            {"email": "noexist@test.com", "password": "testpass123"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class EventIngestEndpointTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.ingest_url = "/api/events/ingest/"
        self.user = User.objects.create_user(
            email="event@test.com",
            username="eventuser",
            password="testpass123"
        )
        # Login to get token
        login_response = self.client.post(
            "/api/auth/login/",
            {"email": "event@test.com", "password": "testpass123"},
            format="json"
        )
        self.token = login_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_create_event(self):
        response = self.client.post(
            self.ingest_url,
            {
                "source_name": "Test Source",
                "event_type": "click",
                "payload": {"button": "test"}
            },
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_event_without_auth(self):
        self.client.credentials()  # Remove auth
        response = self.client.post(
            self.ingest_url,
            {
                "source_name": "Test Source",
                "event_type": "click",
                "payload": {"button": "test"}
            },
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class MetricsEndpointTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="metrics@test.com",
            username="metricsuser",
            password="testpass123"
        )
        login_response = self.client.post(
            "/api/auth/login/",
            {"email": "metrics@test.com", "password": "testpass123"},
            format="json"
        )
        self.token = login_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_summary_requires_auth(self):
        self.client.credentials()  # Remove auth
        response = self.client.get("/api/metrics/summary/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_summary_with_auth(self):
        response = self.client.get("/api/metrics/summary/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
