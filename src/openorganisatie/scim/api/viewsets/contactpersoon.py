from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from openorganisatie.scim.models.contactpersoon import Contactpersoon
from openorganisatie.utils.scim_middleware import BearerTokenAuthentication

from ..filterset.contactpersoon import ContactpersoonFilter
from ..serializers.contactpersoon import ContactpersoonSerializer


@extend_schema(tags=["Contactpersonen"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle contactpersonen opvragen.",
        description="Deze lijst kan gefilterd worden met query-string parameters.",
    ),
    retrieve=extend_schema(
        summary="Een specifieke contactpersoon opvragen.",
        description="Een specifieke contactpersoon opvragen via UUID.",
    ),
)
class ContactpersoonReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Contactpersoon.objects.all()
    serializer_class = ContactpersoonSerializer
    filterset_class = ContactpersoonFilter
    lookup_field = "uuid"
    authentication_classes = (BearerTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
