import uuid

import factory

from openorganisatie.scim.models.team import Team


class TeamFactory(factory.django.DjangoModelFactory):
    uuid = factory.LazyFunction(uuid.uuid4)
    name = factory.Sequence(lambda n: f"Team {n}")
    description = factory.Faker("sentence")

    class Meta:
        model = Team
