from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.test import RequestFactory, TestCase
from django.urls import reverse

from rest_framework.authtoken.models import Token

from ..scim_middleware import SCIMTokenAuthMiddleware


class SCIMTokenAuthMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.get_response = lambda request: JsonResponse({"success": True})
        self.middleware = SCIMTokenAuthMiddleware(self.get_response)

        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.token, _ = Token.objects.get_or_create(user=self.user)

        self.scim_users_url = reverse("scim:users")

    def test_scim_path_with_valid_token(self):
        auth_header = f"Bearer {self.token.key}"
        request = self.factory.get(self.scim_users_url, HTTP_AUTHORIZATION=auth_header)
        response = self.middleware(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"success": True})
        self.assertEqual(request.user, self.user)
        self.assertEqual(request.auth.key, self.token.key)

    def test_scim_path_with_no_token(self):
        request = self.factory.get(self.scim_users_url)
        response = self.middleware(request)

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {"detail": "Authentication credentials were not provided."},
        )
