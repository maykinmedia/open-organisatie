from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from openorganisatie.scim.models.user import User
from openorganisatie.utils.bearer import BearerTokenAuthentication

from ..filterset.user import UserFilter
from ..serializers.user import UserSerializer


@extend_schema(tags=["Users"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle users opvragen.",
        description="Deze lijst kan gefilterd wordt met query-string parameters.",
    ),
    retrieve=extend_schema(
        summary="Een specifieke user opvragen.",
        description="Een specifieke user opvragen.",
    ),
)
class UserReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_class = UserFilter
    lookup_field = "scim_external_id"
    authentication_classes = (BearerTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
