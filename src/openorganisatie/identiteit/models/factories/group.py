import uuid

import factory

from openorganisatie.identiteit.models.group import Group


class GroupFactory(factory.django.DjangoModelFactory):
    scim_external_id = factory.LazyFunction(uuid.uuid4)
    name = factory.Sequence(lambda n: f"Team {n}")
    description = factory.Faker("sentence")

    class Meta:
        model = Group
