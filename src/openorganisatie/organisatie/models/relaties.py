from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import DateRangeField
from django.contrib.postgres.fields.ranges import RangeOperators
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class FunctieTeam(models.Model):
    functie = models.ForeignKey("organisatie.Functie", on_delete=models.CASCADE)
    team = models.ForeignKey("organisatie.Team", on_delete=models.CASCADE)

    wijzigingsdatum = models.DateTimeField(auto_now=True)

    geldigheid = DateRangeField(
        help_text=_("Geldigheidsperiode van deze relatie."),
    )

    class Meta:
        verbose_name = _("Functie Team")
        verbose_name_plural = _("Functie teams")

        constraints = [
            ExclusionConstraint(
                name="no_overlapping_functie_team_geldigheid",
                expressions=[
                    ("functie", RangeOperators.EQUAL),
                    ("team", RangeOperators.EQUAL),
                    ("geldigheid", RangeOperators.OVERLAPS),
                ],
            ),
        ]

    def __str__(self):
        return f"{self.functie} - {self.team}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()

        if not self.geldigheid:
            return

        qs = FunctieTeam.objects.filter(
            functie_id=self.functie_id,
            team_id=self.team_id,
        ).exclude(pk=self.pk)

        if qs.filter(geldigheid__overlap=self.geldigheid).exists():
            raise ValidationError(
                {"geldigheid": "Deze geldigheid overlapt met een bestaande toewijzing."}
            )


class OrganisatorischeEenheidFunctie(models.Model):
    functie = models.ForeignKey("organisatie.Functie", on_delete=models.CASCADE)
    organisatorische_eenheid = models.ForeignKey(
        "organisatie.OrganisatorischeEenheid", on_delete=models.CASCADE
    )

    wijzigingsdatum = models.DateTimeField(auto_now=True)

    geldigheid = DateRangeField(
        help_text=_("Geldigheidsperiode van deze relatie."),
    )

    class Meta:
        verbose_name = _("Functie organisatorische eenheden")
        verbose_name_plural = _("Functie organisatorische eenheden")

        constraints = [
            ExclusionConstraint(
                name="no_overlapping_organisatie_functie_geldigheid",
                expressions=[
                    ("functie", RangeOperators.EQUAL),
                    ("organisatorische_eenheid", RangeOperators.EQUAL),
                    ("geldigheid", RangeOperators.OVERLAPS),
                ],
            ),
        ]

    def __str__(self):
        return f"{self.functie} - {self.organisatorische_eenheid}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()

        if not self.geldigheid:
            return

        qs = OrganisatorischeEenheidFunctie.objects.filter(
            functie_id=self.functie_id,
            organisatorische_eenheid_id=self.organisatorische_eenheid_id,
        ).exclude(pk=self.pk)

        if qs.filter(geldigheid__overlap=self.geldigheid).exists():
            raise ValidationError(
                {"geldigheid": "Deze geldigheid overlapt met een bestaande toewijzing."}
            )
