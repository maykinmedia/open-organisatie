from psycopg.types.range import DateRange
from rest_framework import serializers

from ..models.relaties import FunctieTeam, OrganisatorischeEenheidFunctie


def build_period_range(period):
    start = period.get("startdatum")
    end = period.get("einddatum")

    if not start:
        raise serializers.ValidationError({"teams_input": "Startdatum is verplicht."})

    if end and start > end:
        raise serializers.ValidationError(
            {"teams_input": "Einddatum moet na startdatum liggen."}
        )

    return DateRange(start, end)


def validate_functie_team(serializer, attrs):
    functie = getattr(serializer.instance, "pk", None) and serializer.instance
    teams = attrs.get("teams_input", [])

    for item in teams:
        team = item.get("team")
        period = item.get("periode")

        if not team or not period:
            continue

        period_range = build_period_range(period)

        qs = FunctieTeam.objects.filter(
            # functie=functie,
            team=team,
        )

        if functie:
            qs = qs.filter(functie=functie)

        if qs.filter(periode__overlap=period_range).exists():
            raise serializers.ValidationError(
                {"teams_input": "Deze periode overlapt met een bestaand team."}
            )


def validate_functie_oe(serializer, attrs):
    functie = getattr(serializer.instance, "pk", None) and serializer.instance
    organisatorische_eenheden = attrs.get("organisatorische_eenheden_input", [])

    for item in organisatorische_eenheden:
        organisatorische_eenheid = item.get("organisatorische_eenheid")
        period = item.get("periode")

        if not organisatorische_eenheid or not period:
            continue

        period_range = build_period_range(period)

        qs = OrganisatorischeEenheidFunctie.objects.filter(
            organisatorische_eenheid=organisatorische_eenheid,
        )

        if functie:
            qs = qs.filter(functie=functie)

        if qs.filter(periode__overlap=period_range).exists():
            raise serializers.ValidationError(
                {
                    "organisatorische_eenheden_input": "Deze periode overlapt met een bestaande relatie."
                }
            )
