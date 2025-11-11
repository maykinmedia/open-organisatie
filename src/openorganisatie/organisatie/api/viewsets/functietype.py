from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from reversion.views import RevisionMixin

from openorganisatie.organisatie.models.functietype import FunctieType

from ..serializers.functietype import FunctieTypeSerializer


@extend_schema(tags=["Functietypes"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle functietypes opvragen.",
        description="Deze lijst kan gefilterd worden met query-string parameters.",
    ),
    retrieve=extend_schema(
        summary="Een specifiek functietype opvragen.",
        description="Een specifiek functietype opvragen via UUID.",
    ),
    create=extend_schema(
        summary="Nieuw functietype aanmaken.",
        description="Voeg een nieuw functietype toe aan het systeem.",
    ),
    update=extend_schema(
        summary="Functietype volledig bijwerken.",
        description="Werk alle gegevens van een functietype bij.",
    ),
    partial_update=extend_schema(
        summary="Functietype gedeeltelijk bijwerken.",
        description="Werk enkele gegevens van een functietype bij.",
    ),
    destroy=extend_schema(
        summary="Functietype verwijderen.",
        description="Verwijder een specifiek functietype.",
    ),
)
class FunctieTypeViewSet(RevisionMixin, viewsets.ModelViewSet):
    queryset = FunctieType.objects.all()
    serializer_class = FunctieTypeSerializer
    filterset_fields = {
        "naam",
        "slug",
    }
    lookup_field = "uuid"
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
