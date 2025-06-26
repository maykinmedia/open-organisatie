import uuid

from django.db import models

from django_scim.models import AbstractSCIMCommonAttributesMixin


class Medewerker(AbstractSCIMCommonAttributesMixin, models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
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

    def save(self, *args, **kwargs):
        if not self.scim_id:
            self.scim_id = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def is_active(self):
        return self.actief and not self.datum_uit_dienst

    @property
    def scim_username(self):
        return self.emailadres

    @scim_username.setter
    def scim_username(self, value):
        self.emailadres = value
