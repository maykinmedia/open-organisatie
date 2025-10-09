import uuid

from django.utils import timezone

import factory

from openorganisatie.scim.enums.enums import GenderIndicator
from openorganisatie.scim.models import Medewerker


class MedewerkerFactory(factory.django.DjangoModelFactory):
    uuid = factory.LazyFunction(uuid.uuid4)
    medewerker_id = factory.Sequence(lambda n: f"medewerker_{n}")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.LazyAttribute(
        lambda obj: f"{obj.first_name.lower()}.{obj.last_name.lower()}@example.com"
    )
    phone_number = factory.Faker("phone_number")
    gender_indicator = gender_indicator = factory.Iterator(
        [choice[0] for choice in GenderIndicator.choices]
    )
    termination_date = None
    date_joined = factory.LazyFunction(timezone.now)

    class Meta:
        model = Medewerker

    @factory.post_generation
    def teams(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.teams.set(extracted)

    @factory.post_generation
    def organisatorische_eenheden(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.organisatorische_eenheden.set(extracted)

    @factory.post_generation
    def functies(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.functies.set(extracted)
