import uuid

from django.utils import timezone

import factory

from openorganisatie.identiteit.models.user import User


class UserFactory(factory.django.DjangoModelFactory):
    scim_external_id = factory.LazyFunction(uuid.uuid4)
    username = factory.Faker("first_name")
    email = factory.LazyAttribute(
        lambda obj: f"{obj.first_name.lower()}.{obj.last_name.lower()}@example.com"
    )
    is_active = True
    date_joined = factory.LazyFunction(timezone.now)
    last_modified = factory.LazyFunction(timezone.now)

    class Meta:
        model = User
