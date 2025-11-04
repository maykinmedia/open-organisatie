from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from reversion.views import RevisionMixin

from openorganisatie.scim.models.vestiging import Vestiging
from openorganisatie.utils.bearer import BearerTokenAuthentication

from ..serializers.vestiging import VestigingSerializer


@extend_schema(tags=["Vestigingen"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle vestigingen opvragen.",
        description="Deze lijst kan gefilterd worden met query-string parameters.",
    ),
    retrieve=extend_schema(
        summary="Een specifieke vestiging opvragen.",
        description="Een specifieke vestiging opvragen aan de hand van het vestigingsnummer.",
    ),
    create=extend_schema(
        summary="Nieuwe vestiging aanmaken.",
        description="Voeg een nieuwe vestiging toe aan het systeem.",
    ),
    update=extend_schema(
        summary="Vestiging volledig bijwerken.",
        description="Werk alle gegevens van een vestiging bij.",
    ),
    partial_update=extend_schema(
        summary="Vestiging gedeeltelijk bijwerken.",
        description="Werk enkele gegevens van een vestiging bij.",
    ),
    destroy=extend_schema(
        summary="Vestiging verwijderen.",
        description="Verwijder een specifieke vestiging.",
    ),
)
class VestigingViewSet(RevisionMixin, viewsets.ModelViewSet):
    queryset = Vestiging.objects.all()
    serializer_class = VestigingSerializer
    filterset_fields = {
        "naam",
        "vestigingsnummer",
        "verkorte_naam",
        "adres",
        "post_adres",
        "landcode",
    }
    lookup_field = "uuid"
    authentication_classes = (BearerTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
