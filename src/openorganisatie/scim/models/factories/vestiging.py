import uuid

import factory

from openorganisatie.scim.models import Vestiging


class VestigingFactory(factory.django.DjangoModelFactory):
    uuid = factory.LazyFunction(uuid.uuid4)
    vestigingsnummer = factory.Faker("bothify", text="B###")
    naam = factory.Faker("company")
    verkorte_naam = factory.Faker("company_suffix")
    adres = factory.Faker("address")
    correspondentieadres = factory.Faker("address")
    post_adres = factory.Faker("postcode")
    telefoonnummer = factory.Faker("phone_number")
    landcode = factory.Faker("country_code")

    class Meta:
        model = Vestiging
