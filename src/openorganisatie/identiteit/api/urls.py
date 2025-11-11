from django.urls import include, path

from drf_spectacular.views import (
    SpectacularRedocView,
)
from vng_api_common import routers

from ...utils.views import SpectacularJSONAPIView, SpectacularYAMLAPIView
from .schema import custom_settings
from .viewsets.group import GroupReadOnlyViewSet
from .viewsets.user import UserReadOnlyViewSet

app_name = "identiteit_api"

router = routers.DefaultRouter()

router.register("users", UserReadOnlyViewSet)
router.register("groups", GroupReadOnlyViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("", router.APIRootView.as_view(), name="root"),
    path(
        "openapi.json",
        SpectacularJSONAPIView.as_view(
            urlconf="openorganisatie.identiteit.api.urls",
            custom_settings=custom_settings,
        ),
        name="schema-json-identiteit",
    ),
    path(
        "openapi.yaml",
        SpectacularYAMLAPIView.as_view(
            urlconf="openorganisatie.identiteit.api.urls",
            custom_settings=custom_settings,
        ),
        name="schema-yaml-identiteit",
    ),
    path(
        "schema/",
        SpectacularRedocView.as_view(
            url_name="identiteit_api:schema-yaml-identiteit",
        ),
        name="schema-redoc-identiteit",
    ),
]
