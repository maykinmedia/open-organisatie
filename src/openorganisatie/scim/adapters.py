from django_scim.adapters import SCIMUser

from .models.medewerker import Medewerker


class MedewerkerAdapter(SCIMUser):
    model = Medewerker
    id_field = "azure_oid"
    url_name = "scim:user-detail"

    def delete(self, *args, **kwargs):
        self.model.objects.filter(**{self.id_field: self.id}).delete()

    @property
    def groups(self):
        return []

    def to_dict(self):
        d = super().to_dict()

        d.update(
            {
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
        )

        return d

    def from_dict(self, d):
        super().from_dict(d)

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

        phone_numbers = d.get("phoneNumbers", [])
        if phone_numbers:
            self.obj.telefoonnummer = phone_numbers[0].get("value", "")

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
