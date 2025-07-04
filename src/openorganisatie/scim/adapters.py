from django_scim import constants
from django_scim.adapters import SCIMUser

from .models.medewerker import Medewerker


class MedewerkerAdapter(SCIMUser):
    model = Medewerker
    id_field = "azure_oid"
    url_name = "scim:user-detail"

    def delete(self, *args, **kwargs):
        self.model.objects.filter(**{self.id_field: self.id}).delete()

    @property
    def meta(self):
        return {
            "created": self.obj.datum_toegevoegd.isoformat()
            if self.obj.datum_toegevoegd
            else None,
            "lastModified": self.obj.laatst_gewijzigd.isoformat()
            if self.obj.laatst_gewijzigd
            else None,
        }

    @property
    def groups(self):
        return []

    def to_dict(self):
        return {
            "schemas": [constants.SchemaURI.USER],
            "id": str(self.obj.azure_oid),
            "userName": str(self.obj.azure_oid),
            "name": {
                "givenName": self.obj.voornaam,
                "familyName": self.obj.achternaam,
            },
            "active": self.obj.actief,
            "emails": [{"value": self.obj.emailadres}],
            "phoneNumbers": [{"value": self.obj.telefoonnummer}],
            "jobTitle": self.obj.functie,
            "meta": self.meta,
            "groups": self.groups,
        }

    def from_dict(self, d):
        self.obj.azure_oid = d.get("userName", self.obj.azure_oid)

        name = d.get("name", {})
        if name:
            self.obj.voornaam = name.get("givenName", "")
            self.obj.achternaam = name.get("familyName", "")
        else:
            display_name = d.get("displayName", "")
            if display_name:
                parts = display_name.split(" ", 1)
                self.obj.voornaam = parts[0]
                if len(parts) > 1:
                    self.obj.achternaam = parts[1]
                else:
                    self.obj.achternaam = ""

        emails = d.get("emails", [])
        if emails:
            work_email = next(
                (email.get("value") for email in emails if email.get("type") == "work"),
                None,
            )
            other_email = next(
                (
                    email.get("value")
                    for email in emails
                    if email.get("type") == "other"
                ),
                None,
            )
            upn = d.get("userPrincipalName")
            self.obj.emailadres = (
                work_email or other_email or upn or emails[0].get("value", "")
            )

        phone_numbers = d.get("phoneNumbers", [])
        if phone_numbers:
            self.obj.telefoonnummer = phone_numbers[0].get("value", "")

        self.obj.actief = d.get("active", True)  # if default=True

        job_title = d.get("jobTitle")
        if job_title is not None:
            self.obj.functie = job_title

        self.obj.save()

    def handle_operations(self, operations):
        for op in operations:
            operation = op["op"].lower()
            path = op.get("path", "").lower()
            value = op.get("value")

            if operation in ("replace", "add"):
                if path == "active":
                    self.obj.actief = bool(value)
                elif path == "userName":
                    self.obj.azure_oid = value
            elif operation == "remove":
                if path == "userName":
                    self.obj.azure_oid = ""

        self.obj.save()
