from django.urls import include, path

from drf_spectacular.views import (
    SpectacularJSONAPIView,
    SpectacularRedocView,
    SpectacularYAMLAPIView,
)
from vng_api_common import routers

from .schema import custom_settings
from .viewsets.contactpersoon import ContactpersoonViewSet
from .viewsets.group import GroupReadOnlyViewSet
from .viewsets.medewerker import MedewerkerViewSet
from .viewsets.organisatorische_eenheid import OrganisatorischeEenheidViewSet
from .viewsets.team import TeamViewSet
from .viewsets.user import UserReadOnlyViewSet
from .viewsets.vestiging import VestigingViewSet

app_name = "scim_api"

router = routers.DefaultRouter()
router.register("medewerkers", MedewerkerViewSet)
router.register("contactpersoon", ContactpersoonViewSet)
router.register("vestiging", VestigingViewSet)
router.register("organisatorische-eenheid", OrganisatorischeEenheidViewSet)
router.register("teams", TeamViewSet)
router.register("users", UserReadOnlyViewSet)
router.register("groups", GroupReadOnlyViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("", router.APIRootView.as_view(), name="root"),
    path(
        "schema/openapi.json",
        SpectacularJSONAPIView.as_view(
            urlconf="openorganisatie.scim.api.urls",
            custom_settings=custom_settings,
        ),
        name="schema-json-medewerkers",
    ),
    path(
        "schema/openapi.yaml",
        SpectacularYAMLAPIView.as_view(
            urlconf="openorganisatie.scim.api.urls",
            custom_settings=custom_settings,
        ),
        name="schema-yaml-medewerkers",
    ),
    path(
        "schema/",
        SpectacularRedocView.as_view(
            url_name="scim_api:schema-yaml-medewerkers",
        ),
        name="schema-redoc-medewerkers",
    ),
]
