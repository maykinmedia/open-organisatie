from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from reversion.views import RevisionMixin

from openorganisatie.organisatie.models.functie import Functie

from ..filterset.functie import FunctieFilter
from ..serializers.functie import FunctieSerializer


@extend_schema(tags=["Functies"])
@extend_schema_view(
    list=extend_schema(
        summary="Alle functies opvragen.",
        description="Deze lijst kan gefilterd worden met query-string parameters.",
    ),
    retrieve=extend_schema(
        summary="Een specifieke functie opvragen.",
        description="Een specifieke functie opvragen via UUID.",
    ),
    create=extend_schema(
        summary="Nieuwe functie aanmaken.",
        description="Voeg een nieuwe functie toe aan het systeem.",
    ),
    update=extend_schema(
        summary="Functie volledig bijwerken.",
        description="Werk alle gegevens van een functie bij.",
    ),
    partial_update=extend_schema(
        summary="Functie gedeeltelijk bijwerken.",
        description="Werk enkele gegevens van een functie bij.",
    ),
    destroy=extend_schema(
        summary="Functie verwijderen.",
        description="Verwijder een specifieke functie.",
    ),
)
class FunctieViewSet(RevisionMixin, viewsets.ModelViewSet):
    queryset = Functie.objects.all()
    serializer_class = FunctieSerializer
    filterset_class = FunctieFilter
    lookup_field = "uuid"
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
