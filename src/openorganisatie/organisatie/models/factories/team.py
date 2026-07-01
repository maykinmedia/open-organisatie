import uuid

from factory.declarations import LazyFunction, Sequence, SubFactory
from factory.django import DjangoModelFactory
from factory.faker import Faker
from factory.helpers import post_generation

from openorganisatie.organisatie.models.team import Team

from .medewerker import MedewerkerFactory


class TeamFactory(DjangoModelFactory):
    external_id = LazyFunction(uuid.uuid4)
    uuid = LazyFunction(uuid.uuid4)
    naam = Sequence(lambda n: f"Team {n}")
    omschrijving = Faker("sentence")
    contactpersoon = SubFactory(MedewerkerFactory)

    class Meta:  # type: ignore[override]
        model = Team

    @post_generation
    def vestigingen(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.vestigingen.set(extracted)  # type: ignore[attr-defined]
