import uuid

import factory

from openorganisatie.scim.models.organisatorische_eenheid import OrganisatorischeEenheid


class OrganisatorischeEenheidFactory(factory.django.DjangoModelFactory):
    uuid = factory.LazyFunction(uuid.uuid4)
    identifier = factory.Faker("bothify", text="OE###")
    name = factory.Faker("company")
    organization_type = factory.Faker("job")
    short_name = factory.Faker("company_suffix")
    description = factory.Faker("catch_phrase")
    email_address = factory.Faker("email")
    phone_number = factory.Faker("phone_number")
    end_date = None

    class Meta:
        model = OrganisatorischeEenheid
