from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from ..models.relaties import FunctieTeam, OrganisatorischeEenheidFunctie


def validate_functie_team(serializer, attrs):
    functie = getattr(serializer.instance, "pk", None) and serializer.instance
    teams = attrs.get("teams_input", [])

    for item in teams:
        team = item.get("team")
        geldigheid = item.get("geldigheid")

        if not team or not geldigheid:
            continue

        qs = FunctieTeam.objects.filter(
            team=team,
        )

        if functie:
            qs = qs.filter(functie=functie)

        if qs.filter(geldigheid__overlap=geldigheid).exists():
            raise serializers.ValidationError(
                {"teams_input": _("Deze geldigheid overlapt met een bestaand team.")}
            )


def validate_functie_oe(serializer, attrs):
    functie = getattr(serializer.instance, "pk", None) and serializer.instance
    organisatorische_eenheden = attrs.get("organisatorische_eenheden_input", [])

    for item in organisatorische_eenheden:
        organisatorische_eenheid = item.get("organisatorische_eenheid")
        geldigheid = item.get("geldigheid")

        if not organisatorische_eenheid or not geldigheid:
            continue

        qs = OrganisatorischeEenheidFunctie.objects.filter(
            organisatorische_eenheid=organisatorische_eenheid,
        )

        if functie:
            qs = qs.filter(functie=functie)

        if qs.filter(geldigheid__overlap=geldigheid).exists():
            raise serializers.ValidationError(
                {
                    "organisatorische_eenheden_input": _(
                        "Deze geldigheid overlapt met een bestaande relatie."
                    )
                }
            )
