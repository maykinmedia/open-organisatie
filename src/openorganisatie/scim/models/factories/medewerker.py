import uuid

from django.utils import timezone

import factory

from openorganisatie.scim.models import Medewerker


class MedewerkerFactory(factory.django.DjangoModelFactory):
    username = factory.LazyFunction(uuid.uuid4)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.LazyAttribute(
        lambda obj: f"{obj.first_name.lower()}.{obj.last_name.lower()}@example.com"
    )
    job_title = factory.Faker("job")
    phone_number = factory.Faker("phone_number")
    gender_indicator = factory.Faker("boolean")
    termination_date = None
    is_active = True
    date_joined = factory.LazyFunction(timezone.now)

    class Meta:
        model = Medewerker
