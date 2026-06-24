import uuid

from factory.declarations import LazyFunction, Sequence
from factory.django import DjangoModelFactory
from factory.faker import Faker

from openorganisatie.identiteit.models.group import Group


class GroupFactory(DjangoModelFactory):
    scim_external_id = LazyFunction(uuid.uuid4)
    name = Sequence(lambda n: f"Team {n}")
    description = Faker("sentence")
    active = True

    class Meta:  # type: ignore
        model = Group
