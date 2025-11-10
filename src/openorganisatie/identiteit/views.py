from django_scim.views import GroupsView, UsersView

from .adapters import GroupAdapter, UserAdapter
from .models.group import Group
from .models.user import User


class MedewerkerUsersView(UsersView):
    @classmethod
    def scim_adapter_getter(cls):
        return UserAdapter

    @classmethod
    def model_cls_getter(cls):
        return User


class GroepenView(GroupsView):
    @classmethod
    def scim_adapter_getter(cls):
        return GroupAdapter

    @classmethod
    def model_cls_getter(cls):
        return Group
