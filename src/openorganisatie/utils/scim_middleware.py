from django.http import JsonResponse

from rest_framework.exceptions import AuthenticationFailed

from .bearer import BearerTokenAuthentication


class SCIMTokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.auth = BearerTokenAuthentication()

    def __call__(self, request):
        if request.path.startswith("/scim/"):
            try:
                user_auth_tuple = self.auth.authenticate(request)
                if user_auth_tuple is None:
                    raise AuthenticationFailed(
                        "Authentication credentials were not provided."
                    )
                request.user, request.auth = user_auth_tuple
            except AuthenticationFailed:
                return JsonResponse(
                    {"detail": "Authentication credentials were not provided."},
                    status=401,
                )

        response = self.get_response(request)
        return response
