import uuid

import factory

from openorganisatie.organisatie.models import Vestiging


class VestigingFactory(factory.django.DjangoModelFactory):
    external_id = factory.LazyFunction(uuid.uuid4)
    uuid = factory.LazyFunction(uuid.uuid4)
    vestigingsnummer = factory.Faker("bothify", text="B###")
    naam = factory.Faker("company")
    adres = factory.Faker("address")
    correspondentieadres = factory.Faker("address")
    post_adres = factory.Faker("postcode")
    telefoonnummer = factory.Faker("phone_number")

    class Meta:
        model = Vestiging
