from django.urls import include, path

from drf_spectacular.views import (
    SpectacularRedocView,
)
from vng_api_common import routers

from ...utils.views import SpectacularJSONAPIView, SpectacularYAMLAPIView
from .schema import custom_settings
from .viewsets.contactpersoon import ContactpersoonReadOnlyViewSet
from .viewsets.group import GroupReadOnlyViewSet
from .viewsets.medewerker import MedewerkerReadOnlyViewSet
from .viewsets.organisatorische_eenheid import OrganisatorischeEenheidReadOnlyViewSet
from .viewsets.team import TeamReadOnlyViewSet
from .viewsets.user import UserReadOnlyViewSet
from .viewsets.vestiging import VestigingReadOnlyViewSet

app_name = "scim_api"

router = routers.DefaultRouter()
router.register("medewerkers", MedewerkerReadOnlyViewSet)
router.register("contactpersoon", ContactpersoonReadOnlyViewSet)
router.register("vestiging", VestigingReadOnlyViewSet)
router.register("organisatorische-eenheid", OrganisatorischeEenheidReadOnlyViewSet)
router.register("teams", TeamReadOnlyViewSet)
router.register("users", UserReadOnlyViewSet)
router.register("groups", GroupReadOnlyViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("", router.APIRootView.as_view(), name="root"),
    path(
        "openapi.json",
        SpectacularJSONAPIView.as_view(
            urlconf="openorganisatie.scim.api.urls",
            custom_settings=custom_settings,
        ),
        name="schema-json-medewerkers",
    ),
    path(
        "openapi.yaml",
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
