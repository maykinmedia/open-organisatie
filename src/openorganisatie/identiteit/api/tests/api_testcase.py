from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

User = get_user_model()


class APITestCase(TestCase):
    auth_type = "Token"

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"{self.auth_type} {self.token.key}")


class APITestCaseBearer(APITestCase):
    auth_type = "Bearer"
