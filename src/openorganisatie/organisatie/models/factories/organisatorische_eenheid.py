import random
import uuid
from datetime import timedelta

from django.utils import timezone

from factory.declarations import LazyAttribute, LazyFunction, Sequence, SubFactory
from factory.django import DjangoModelFactory
from factory.faker import Faker
from factory.helpers import post_generation

from openorganisatie.organisatie.models.organisatorische_eenheid import (
    OrganisatorischeEenheid,
)

from .medewerker import MedewerkerFactory


class OrganisatorischeEenheidFactory(DjangoModelFactory):
    external_id = LazyFunction(uuid.uuid4)
    uuid = LazyFunction(uuid.uuid4)
    identificatie = Sequence(lambda n: f"OE{n:03d}")
    naam = Sequence(lambda n: f"Organisatie {n}")
    soort_organisatie = Faker("word")
    verkorte_naam = Faker("word")
    omschrijving = Faker("text", max_nb_chars=50)
    emailadres = Sequence(lambda n: f"user{n}@example.com")
    telefoonnummer = Faker("phone_number")
    startdatum = LazyFunction(timezone.now)
    einddatum = LazyAttribute(
        lambda obj: obj.startdatum + timedelta(days=random.randint(1, 30))
    )
    hoofd_organisatorische_eenheid = None
    contactpersoon = SubFactory(MedewerkerFactory)

    class Meta:  # type: ignore[override]
        model = OrganisatorischeEenheid

    @post_generation
    def vestigingen(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.vestigingen.set(extracted)  # type: ignore[attr-defined]
