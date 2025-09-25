from django.db import models


class Functie(models.Model):
    functie_omschrijving = models.CharField(max_length=255)
    begin_datum = models.DateField()
    eind_datum = models.DateField()
    functie_type = models.ForeignKey(
        "scim.FunctieType", on_delete=models.CASCADE, related_name="functies"
    )

    class Meta:
        verbose_name = "Functie"
        verbose_name_plural = "Functies"

    def __str__(self):
        return self.functie_omschrijving
