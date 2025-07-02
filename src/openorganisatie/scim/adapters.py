from django_scim.adapters import SCIMUser

from .models.medewerker import Medewerker


class MedewerkerAdapter(SCIMUser):
    model = Medewerker
    id_field = "azure_oid"

    def delete(self, *args, **kwargs):
        self.model.objects.filter(**{self.id_field: self.id}).delete()

    @property
    def display_name(self):
        return f"{self.obj.voornaam} {self.obj.achternaam}"

    @property
    def emails(self):
        return [{"value": self.obj.emailadres, "primary": True}]

    @property
    def groups(self):
        return []

    def to_dict(self):
        return {
            "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
            "id": str(self.obj.azure_oid),
            "userName": str(self.obj.azure_oid),
            "name": {
                "givenName": self.obj.voornaam,
                "familyName": self.obj.achternaam,
                "formatted": self.display_name,
            },
            "displayName": self.display_name,
            "emails": self.emails,
            "active": self.obj.actief,
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
            self.obj.emailadres = emails[0].get("value", "")

        phone_numbers = d.get("phoneNumbers", [])
        if phone_numbers:
            self.obj.telefoonnummer = phone_numbers[0].get("value", "")

        active = d.get("active")
        if active is not None:
            self.obj.actief = active

        self.obj.functie = d.get("functie", self.obj.functie)

        self.obj.save()

    def handle_operations(self, operations):
        for op in operations:
            operation = op["op"].lower()
            path = (op.get("path") or "").lower()
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
