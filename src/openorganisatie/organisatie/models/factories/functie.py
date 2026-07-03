import uuid
from datetime import date, timedelta

from factory.declarations import LazyFunction, SubFactory
from factory.django import DjangoModelFactory
from factory.faker import Faker
from factory.helpers import post_generation
from psycopg.types.range import DateRange

from openorganisatie.organisatie.models.functie import Functie
from openorganisatie.organisatie.models.functietype import (
    FunctieType,
)

from ..relaties import FunctieTeam, OrganisatorischeEenheidFunctie
from .medewerker import MedewerkerFactory
from .organisatorische_eenheid import OrganisatorischeEenheidFactory
from .team import TeamFactory


class FunctieTypeFactory(DjangoModelFactory):
    external_id = LazyFunction(uuid.uuid4)
    naam = Faker("word")
    slug = Faker("slug")

    class Meta:  # type: ignore[override]
        model = FunctieType


class FunctieTeamFactory(DjangoModelFactory):
    functie = SubFactory(
        "openorganisatie.organisatie.models.factories.functie.FunctieFactory"
    )
    team = SubFactory(TeamFactory)

    geldigheid = LazyFunction(
        lambda: DateRange(
            date.today(),
            date.today() + timedelta(days=30),
        )
    )

    class Meta:  # type: ignore[override]
        model = FunctieTeam


class OrganisatorischeEenheidFunctieFactory(DjangoModelFactory):
    functie = SubFactory(
        "openorganisatie.organisatie.models.factories.functie.FunctieFactory"
    )
    organisatorische_eenheid = SubFactory(OrganisatorischeEenheidFactory)

    geldigheid = LazyFunction(
        lambda: DateRange(
            date.today(),
            date.today() + timedelta(days=30),
        )
    )

    class Meta:  # type: ignore[override]
        model = OrganisatorischeEenheidFunctie


class FunctieFactory(DjangoModelFactory):
    external_id = LazyFunction(uuid.uuid4)
    uuid = LazyFunction(uuid.uuid4)
    functie_omschrijving = Faker("job")
    startdatum = Faker("date_this_decade")
    einddatum = Faker("date_this_decade")
    medewerker = SubFactory(MedewerkerFactory)
    functie_type = SubFactory(FunctieTypeFactory)
    vervanger = None

    class Meta:  # type: ignore[override]
        model = Functie

    @post_generation
    def teams(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for team in extracted:
                FunctieTeamFactory(functie=self, team=team)

    @post_generation
    def organisatorische_eenheden(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for oe in extracted:
                OrganisatorischeEenheidFunctieFactory(
                    functie=self,
                    organisatorische_eenheid=oe,
                )
