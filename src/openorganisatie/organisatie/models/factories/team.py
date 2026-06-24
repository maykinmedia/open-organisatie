import uuid

import factory

from openorganisatie.organisatie.models.team import Team

from .medewerker import MedewerkerFactory


class TeamFactory(factory.django.DjangoModelFactory):
    external_id = factory.LazyFunction(uuid.uuid4)
    uuid = factory.LazyFunction(uuid.uuid4)
    naam = factory.Sequence(lambda n: f"Team {n}")
    omschrijving = factory.Faker("sentence")
    contactpersoon = factory.SubFactory(MedewerkerFactory)

    class Meta:
        model = Team

    @factory.post_generation
    def vestigingen(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.vestigingen.set(extracted)  # type: ignore[attr-defined]
