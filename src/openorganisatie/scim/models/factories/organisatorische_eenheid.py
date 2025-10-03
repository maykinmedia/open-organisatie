import uuid

import factory

from openorganisatie.scim.models.organisatorische_eenheid import OrganisatorischeEenheid


class OrganisatorischeEenheidFactory(factory.django.DjangoModelFactory):
    uuid = factory.LazyFunction(uuid.uuid4)
    identifier = factory.Sequence(lambda n: f"OE{n:03d}")
    name = factory.Faker("company")
    organization_type = factory.Faker("job")
    short_name = factory.Faker("company_suffix")
    description = factory.Faker("text", max_nb_chars=50)
    email_address = factory.Faker("email")
    phone_number = factory.Faker("phone_number")
    end_date = None
    parent_organisation = None

    class Meta:
        model = OrganisatorischeEenheid
