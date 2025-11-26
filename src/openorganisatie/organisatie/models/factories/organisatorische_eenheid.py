import uuid

import factory
from faker import Faker

from openorganisatie.organisatie.models.organisatorische_eenheid import (
    OrganisatorischeEenheid,
)

from .medewerker import MedewerkerFactory

fake = Faker()


class OrganisatorischeEenheidFactory(factory.django.DjangoModelFactory):
    uuid = factory.LazyFunction(uuid.uuid4)
    identificatie = factory.Sequence(lambda n: f"OE{n:03d}")
    naam = factory.LazyAttribute(lambda o: fake.name()[:50])
    soort_organisatie = factory.LazyAttribute(lambda o: fake.job()[:50])
    verkorte_naam = factory.LazyAttribute(lambda o: fake.company_suffix()[:50])
    omschrijving = factory.Faker("text", max_nb_chars=50)
    emailadres = factory.Faker("email")
    telefoonnummer = factory.Faker("phone_number")
    datum_opheffing = None
    hoofd_organisatorische_eenheid = None
    contactpersoon = factory.SubFactory(MedewerkerFactory)

    class Meta:
        model = OrganisatorischeEenheid

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
