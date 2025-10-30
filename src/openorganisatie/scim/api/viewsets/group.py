from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from openorganisatie.scim.models.group import Group

from ..filterset.group import GroupFilter
from ..serializers.group import GroupSerializer


@extend_schema(tags=["Group"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle groups opvragen.",
        description="Deze lijst kan gefilterd wordt met query-string parameters.",
    ),
    retrieve=extend_schema(
        summary="Een specifieke group opvragen.",
        description="Een specifieke group opvragen.",
    ),
)
class GroupReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filterset_class = GroupFilter
    lookup_field = "scim_external_id"
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
