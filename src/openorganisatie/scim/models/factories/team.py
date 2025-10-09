import uuid

import factory

from openorganisatie.scim.models.team import Team


class TeamFactory(factory.django.DjangoModelFactory):
    uuid = factory.LazyFunction(uuid.uuid4)
    name = factory.Sequence(lambda n: f"Team {n}")
    description = factory.Faker("sentence")

    class Meta:
        model = Team

    @factory.post_generation
    def branches(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.branches.set(extracted)

    @factory.post_generation
    def functies(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.functies.set(extracted)
