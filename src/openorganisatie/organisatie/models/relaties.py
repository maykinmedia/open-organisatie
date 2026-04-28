from django.db import models
from django.utils.translation import gettext_lazy as _


class FunctieTeam(models.Model):
    functie = models.ForeignKey("organisatie.Functie", on_delete=models.CASCADE)
    team = models.ForeignKey("organisatie.Team", on_delete=models.CASCADE)

    startdatum = models.DateField(
        help_text=_("De datum waarop de functie begint."),
    )
    einddatum = models.DateField(
        null=True,
        blank=True,
        help_text=_("De datum waarop de functie eindigd."),
    )
    wijzigingsdatum = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Functie Team")
        verbose_name_plural = _("Functie teams")

    def __str__(self):
        return self.team


class OrganisatorischeEenheidFunctie(models.Model):
    functie = models.ForeignKey("organisatie.Functie", on_delete=models.CASCADE)
    organisatorische_eenheid = models.ForeignKey(
        "organisatie.OrganisatorischeEenheid", on_delete=models.CASCADE
    )
    startdatum = models.DateField()
    einddatum = models.DateField(null=True, blank=True)
    wijzigingsdatum = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Functie organisatorische eenheden")
        verbose_name_plural = _("Functie organisatorische eenheden")

    def __str__(self):
        return self.organisatorische_eenheid
