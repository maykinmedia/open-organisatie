import uuid

import factory
from factory import Faker, LazyFunction, SubFactory

from openorganisatie.organisatie.models.functie import Functie
from openorganisatie.organisatie.models.functietype import (
    FunctieType,
)


class FunctieTypeFactory(factory.django.DjangoModelFactory):
    naam = Faker("word")
    slug = Faker("slug")

    class Meta:
        model = FunctieType


class FunctieFactory(factory.django.DjangoModelFactory):
    uuid = LazyFunction(uuid.uuid4)
    functie_omschrijving = Faker("job")
    begin_datum = Faker("date_this_decade")
    eind_datum = Faker("date_this_decade")
    functie_type = SubFactory(FunctieTypeFactory)

    class Meta:
        model = Functie
