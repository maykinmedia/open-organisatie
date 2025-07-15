from django_scim.views import GroupsView, UsersView

from .adapters import GroepenAdapter, MedewerkerAdapter
from .models.medewerker import Medewerker
from .models.team import Team


class MedewerkerUsersView(UsersView):
    @classmethod
    def scim_adapter_getter(cls):
        return MedewerkerAdapter

    @classmethod
    def model_cls_getter(cls):
        return Medewerker


class GroepenView(GroupsView):
    @classmethod
    def scim_adapter_getter(cls):
        return GroepenAdapter

    @classmethod
    def model_cls_getter(cls):
        return Team
