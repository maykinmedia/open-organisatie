from django.db import models


class Medewerker(models.Model):
    medewerker_id = models.CharField(max_length=255, unique=True)
    voornaam = models.CharField(max_length=100)
    achternaam = models.CharField(max_length=100)
    emailadres = models.EmailField(unique=True)
    functie = models.CharField(max_length=100, blank=True)
    telefoonnummer = models.CharField(max_length=30, blank=True)
    geslachtsaanduiding = models.BooleanField(default=True)
    datum_uit_dienst = models.DateField(blank=True, null=True)
    actief = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.voornaam} {self.achternaam}"

    def is_active(self):
        return self.actief and not self.datum_uit_dienst
