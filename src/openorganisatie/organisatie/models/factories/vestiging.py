import uuid

from factory.declarations import LazyFunction
from factory.django import DjangoModelFactory
from factory.faker import Faker

from openorganisatie.organisatie.models import Vestiging


class VestigingFactory(DjangoModelFactory):
    external_id = LazyFunction(uuid.uuid4)
    uuid = LazyFunction(uuid.uuid4)
    vestigingsnummer = Faker("bothify", text="B###")
    naam = Faker("company")
    adres = Faker("address")
    correspondentieadres = Faker("address")
    post_adres = Faker("postcode")
    telefoonnummer = Faker("phone_number")

    class Meta:  # type: ignore
        model = Vestiging
