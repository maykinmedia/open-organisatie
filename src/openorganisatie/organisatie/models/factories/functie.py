import uuid
from datetime import date, timedelta

import factory
from factory import Faker, LazyFunction, SubFactory
from psycopg.types.range import DateRange

from openorganisatie.organisatie.models.functie import Functie
from openorganisatie.organisatie.models.functietype import (
    FunctieType,
)

from ..relaties import FunctieTeam, OrganisatorischeEenheidFunctie
from .medewerker import MedewerkerFactory
from .organisatorische_eenheid import OrganisatorischeEenheidFactory
from .team import TeamFactory


class FunctieTypeFactory(factory.django.DjangoModelFactory):
    external_id = factory.LazyFunction(uuid.uuid4)
    naam = Faker("word")
    slug = Faker("slug")

    class Meta:
        model = FunctieType


class FunctieTeamFactory(factory.django.DjangoModelFactory):
    functie = SubFactory(
        "openorganisatie.organisatie.models.factories.functie.FunctieFactory"
    )
    team = SubFactory(TeamFactory)

    period = factory.LazyFunction(
        lambda: DateRange(
            date.today(),
            date.today() + timedelta(days=30),
        )
    )

    class Meta:
        model = FunctieTeam


class OrganisatorischeEenheidFunctieFactory(factory.django.DjangoModelFactory):
    functie = SubFactory(
        "openorganisatie.organisatie.models.factories.functie.FunctieFactory"
    )
    organisatorische_eenheid = factory.SubFactory(OrganisatorischeEenheidFactory)

    period = factory.LazyFunction(
        lambda: DateRange(
            date.today(),
            date.today() + timedelta(days=30),
        )
    )

    class Meta:
        model = OrganisatorischeEenheidFunctie


class FunctieFactory(factory.django.DjangoModelFactory):
    external_id = factory.LazyFunction(uuid.uuid4)
    uuid = LazyFunction(uuid.uuid4)
    functie_omschrijving = Faker("job")
    startdatum = Faker("date_this_decade")
    einddatum = Faker("date_this_decade")
    medewerker = SubFactory(MedewerkerFactory)
    functie_type = SubFactory(FunctieTypeFactory)

    class Meta:
        model = Functie

    @factory.post_generation
    def teams(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for team in extracted:
                FunctieTeamFactory(functie=self, team=team)

    @factory.post_generation
    def organisatorische_eenheden(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for oe in extracted:
                OrganisatorischeEenheidFunctieFactory(
                    functie=self,
                    organisatorische_eenheid=oe,
                )
