import uuid

import factory

from openorganisatie.scim.models import Vestiging


class VestigingFactory(factory.django.DjangoModelFactory):
    uuid = factory.LazyFunction(uuid.uuid4)
    branchnumber = factory.Faker("bothify", text="B###")
    branchname = factory.Faker("company")
    short_name = factory.Faker("company_suffix")
    address = factory.Faker("address")
    correspondence_address = factory.Faker("address")
    postal_address = factory.Faker("postcode")
    phone_number = factory.Faker("phone_number")
    country_code = factory.Faker("country_code")

    class Meta:
        model = Vestiging
