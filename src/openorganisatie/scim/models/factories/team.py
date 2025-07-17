import uuid

import factory

from openorganisatie.scim.models.team import Team


class TeamFactory(factory.django.DjangoModelFactory):
    scim_id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    scim_external_id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    scim_display_name = factory.LazyAttribute(lambda obj: obj.name)
    name = factory.Sequence(lambda n: f"Team {n}")
    description = factory.Faker("sentence")
    active = True

    class Meta:
        model = Team
