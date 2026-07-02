import random
import uuid
from datetime import timedelta

from django.utils import timezone

from factory.declarations import Iterator, LazyAttribute, LazyFunction, Sequence
from factory.django import DjangoModelFactory
from factory.faker import Faker

from openorganisatie.organisatie.enums.enums import GenderIndicator
from openorganisatie.organisatie.models import Medewerker


class MedewerkerFactory(DjangoModelFactory):
    external_id = LazyFunction(uuid.uuid4)
    uuid = LazyFunction(uuid.uuid4)
    medewerker_id = Sequence(lambda n: f"medewerker_{n}")
    voornaam = Faker("first_name")
    achternaam = Faker("last_name")
    emailadres = Sequence(lambda n: f"user{n}@example.com")
    telefoonnummer = Faker("phone_number")
    geslachtsaanduiding = Iterator([choice[0] for choice in GenderIndicator.choices])
    startdatum = LazyFunction(timezone.now)
    einddatum = LazyAttribute(
        lambda obj: obj.startdatum + timedelta(days=random.randint(1, 30))
    )

    class Meta:  # type: ignore[override]
        model = Medewerker
