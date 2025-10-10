import uuid

import factory

from openorganisatie.scim.models.organisatorische_eenheid import OrganisatorischeEenheid


class OrganisatorischeEenheidFactory(factory.django.DjangoModelFactory):
    uuid = factory.LazyFunction(uuid.uuid4)
    identificatie = factory.Sequence(lambda n: f"OE{n:03d}")
    naam = factory.Faker("name")
    soort_organisatie = factory.Faker("job")
    verkorte_naam = factory.Faker("company_suffix")
    omschrijving = factory.Faker("text", max_nb_chars=50)
    emailadres = factory.Faker("email")
    telefoonnummer = factory.Faker("phone_number")
    datum_opheffing = None
    hoofd_organisatorische_eenheid = None

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
