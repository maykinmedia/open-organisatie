from django.urls import path
from django.views.generic import TemplateView

from django_scim.views import ResourceTypesView

from openorganisatie.identiteit.views import GroepenView, MedewerkerUsersView

app_name = "scim"

urlpatterns = [
    path("", TemplateView.as_view(template_name="master.html"), name="root"),
    path("Users", MedewerkerUsersView.as_view(), name="users"),
    path("Users/<uuid:uuid>", MedewerkerUsersView.as_view(), name="user-detail"),
    path("Groups", GroepenView.as_view(), name="groups"),
    path("Groups/<uuid:uuid>", GroepenView.as_view(), name="group-detail"),
    path(
        "resource-types/<uuid:uuid>", ResourceTypesView.as_view(), name="resource-types"
    ),
]
