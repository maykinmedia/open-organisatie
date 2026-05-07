import uuid

import factory
from factory import Faker, LazyFunction, SubFactory

from openorganisatie.organisatie.models.functie import Functie
from openorganisatie.organisatie.models.functietype import (
    FunctieType,
)


class FunctieTypeFactory(factory.django.DjangoModelFactory):
    external_id = factory.LazyFunction(uuid.uuid4)
    naam = Faker("word")
    slug = Faker("slug")

    class Meta:
        model = FunctieType


class FunctieFactory(factory.django.DjangoModelFactory):
    external_id = factory.LazyFunction(uuid.uuid4)
    uuid = LazyFunction(uuid.uuid4)
    functie_omschrijving = Faker("job")
    startdatum = Faker("date_this_decade")
    einddatum = Faker("date_this_decade")
    functie_type = SubFactory(FunctieTypeFactory)

    class Meta:
        model = Functie
