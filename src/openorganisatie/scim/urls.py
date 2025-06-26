from django.urls import include, path
from django.views.generic import TemplateView

from rest_framework.routers import DefaultRouter

from openorganisatie.scim.views import MedewerkerUsersView

from .viewsets.medewerker import SCIMUserViewSet

router = DefaultRouter()

router.register(r"Users", SCIMUserViewSet, basename="user")

app_name = "scim"

urlpatterns = [
    path("", TemplateView.as_view(template_name="master.html"), name="root"),
    path("Users", MedewerkerUsersView.as_view(), name="users"),
    path("Users/<uuid:uuid>", MedewerkerUsersView.as_view(), name="users"),
    path("", include(("django_scim.urls", "scim"), namespace="scim")),
]
