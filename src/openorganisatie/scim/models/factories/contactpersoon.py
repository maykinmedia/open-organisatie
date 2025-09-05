import uuid

import factory

from openorganisatie.scim.models.contactpersoon import Contactpersoon


class ContactpersoonFactory(factory.django.DjangoModelFactory):
    uuid = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker("name")
    function = factory.Faker("job")
    email_address = factory.LazyAttribute(
        lambda obj: f"{obj.name.lower().replace(' ', '.')}@example.com"
    )
    phone_number = factory.Faker("phone_number")

    class Meta:
        model = Contactpersoon
