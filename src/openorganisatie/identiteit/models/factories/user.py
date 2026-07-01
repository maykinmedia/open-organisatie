import uuid

from django.utils import timezone

from factory.declarations import LazyAttribute, LazyFunction
from factory.django import DjangoModelFactory
from factory.faker import Faker

from openorganisatie.identiteit.models.user import User


class UserFactory(DjangoModelFactory):
    scim_external_id = LazyFunction(uuid.uuid4)
    username = Faker("first_name")
    email = LazyAttribute(lambda obj: f"{obj.username.lower()}@example.com")
    is_active = True
    date_joined = LazyFunction(timezone.now)
    last_modified = LazyFunction(timezone.now)

    class Meta:  # type: ignore[override]
        model = User
