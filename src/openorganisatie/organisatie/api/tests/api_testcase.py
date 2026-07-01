from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase as _APITestCase

from openorganisatie.accounts.tests.factories import UserFactory

User = get_user_model()


class APITestCase(_APITestCase):
    auth_type = "Token"
    user: AbstractBaseUser
    token: Token

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = UserFactory()
        cls.token = Token.objects.create(user=cls.user)

    def setUp(self) -> None:
        super().setUp()
        self.client.credentials(HTTP_AUTHORIZATION=f"{self.auth_type} {self.token.key}")


class APITestCaseBearer(APITestCase):
    auth_type = "Bearer"
