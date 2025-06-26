from django_scim.adapters import SCIMUser

from .models.medewerker import Medewerker


class MedewerkerAdapter(SCIMUser):
    model = Medewerker
    id_field = "uuid"

    def delete(self):
        # Use the correct ID field (uuid) instead of default 'id'
        self.model.objects.filter(**{self.id_field: self.id}).delete()

    @property
    def display_name(self):
        return f"{self.obj.voornaam} {self.obj.achternaam}"

    @property
    def emails(self):
        return [{"value": self.obj.emailadres, "primary": True}]

    @property
    def groups(self):
        # No groups support for this model, return empty list
        return []

    @property
    def meta(self):
        # Add timestamps if your model has them; adjust field names as necessary
        created = getattr(self.obj, "created_at", None)
        updated = getattr(self.obj, "updated_at", None)
        return {
            "resourceType": self.resource_type,
            "created": created.isoformat() if created else None,
            "lastModified": updated.isoformat() if updated else None,
            "location": self.location,
        }

    def to_dict(self):
        return {
            "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
            "id": str(self.obj.uuid),
            "userName": self.obj.emailadres,
            "name": {
                "givenName": self.obj.voornaam,
                "familyName": self.obj.achternaam,
                "formatted": self.display_name,
            },
            "displayName": self.display_name,
            "emails": self.emails,
            "active": self.obj.actief,
            "groups": self.groups,
            "meta": self.meta,
        }

    def from_dict(self, d):
        self.obj.voornaam = d.get("name", {}).get("givenName", "")
        self.obj.achternaam = d.get("name", {}).get("familyName", "")

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
