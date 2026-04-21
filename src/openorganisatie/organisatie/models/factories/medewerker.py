import uuid

from django.utils import timezone

import factory

from openorganisatie.organisatie.enums.enums import GenderIndicator
from openorganisatie.organisatie.models import Medewerker


class MedewerkerFactory(factory.django.DjangoModelFactory):
    external_id = factory.LazyFunction(uuid.uuid4)
    uuid = factory.LazyFunction(uuid.uuid4)
    medewerker_id = factory.Sequence(lambda n: f"medewerker_{n}")
    voornaam = factory.Faker("first_name")
    achternaam = factory.Faker("last_name")
    emailadres = factory.LazyAttribute(
        lambda obj: f"{obj.voornaam.lower()}.{obj.achternaam.lower()}@example.com"
    )
    telefoonnummer = factory.Faker("phone_number")
    geslachtsaanduiding = factory.Iterator(
        [choice[0] for choice in GenderIndicator.choices]
    )
    einddatum = None
    startdatum = factory.LazyFunction(timezone.now)

    class Meta:
        model = Medewerker

    @factory.post_generation
    def teams(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.teams.set(extracted)

    @factory.post_generation
    def functies(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.functies.set(extracted)
