import uuid

import factory

from openorganisatie.organisatie.models.team import Team


class TeamFactory(factory.django.DjangoModelFactory):
    uuid = factory.LazyFunction(uuid.uuid4)
    naam = factory.Sequence(lambda n: f"Team {n}")
    omschrijving = factory.Faker("sentence")

    class Meta:
        model = Team

    @factory.post_generation
    def vestigingen(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.vestigingen.set(extracted)

    @factory.post_generation
    def functies(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.functies.set(extracted)
