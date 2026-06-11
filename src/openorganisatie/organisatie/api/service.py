from psycopg.types.range import DateRange
from rest_framework import serializers

from openorganisatie.organisatie.models.relaties import (
    FunctieTeam,
    OrganisatorischeEenheidFunctie,
)


def update_relations(functie, teams_data, oe_data):
    if teams_data is not None:
        for item in teams_data:
            team = item["team"]
            range_ = item["geldigheid"]

            begin = range_.lower
            end = range_.upper

            rel = (
                FunctieTeam.objects.filter(
                    functie=functie,
                    team=team,
                    geldigheid__upper_inf=True,
                )
                .filter(geldigheid__overlap=range_)
                .first()
            )

            if rel:
                rel.geldigheid = DateRange(rel.geldigheid.lower, end)
                rel.save()
            else:
                qs = FunctieTeam.objects.filter(
                    functie=functie,
                    team=team,
                    geldigheid__overlap=DateRange(begin, end),
                )

                if qs.exists():
                    raise serializers.ValidationError(
                        {
                            "teams_input": "Deze geldigheid overlapt met een bestaand team."
                        }
                    )

                FunctieTeam.objects.create(
                    functie=functie,
                    team=team,
                    geldigheid=DateRange(begin, end),
                )

    if oe_data is not None:
        for item in oe_data:
            oe = item["organisatorische_eenheid"]
            range_ = item["geldigheid"]

            begin = range_.lower
            end = range_.upper

            rel = (
                OrganisatorischeEenheidFunctie.objects.filter(
                    functie=functie,
                    organisatorische_eenheid=oe,
                    geldigheid__upper_inf=True,
                )
                .filter(geldigheid__overlap=range_)
                .first()
            )

            if rel:
                rel.geldigheid = DateRange(rel.geldigheid.lower, end)
                rel.save()
            else:
                qs = OrganisatorischeEenheidFunctie.objects.filter(
                    functie=functie,
                    organisatorische_eenheid=oe,
                    geldigheid__overlap=DateRange(begin, end),
                )

                if qs.exists():
                    raise serializers.ValidationError(
                        {
                            "organisatorische_eenheden_input": (
                                "Deze geldigheid overlapt met een bestaande relatie."
                            )
                        }
                    )
                OrganisatorischeEenheidFunctie.objects.create(
                    functie=functie,
                    organisatorische_eenheid=oe,
                    geldigheid=DateRange(begin, end),
                )
