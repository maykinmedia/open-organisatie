import json
import logging

from django_scim.adapters import SCIMUser

from .models.medewerker import Medewerker

logger = logging.getLogger(__name__)


class MedewerkerAdapter(SCIMUser):
    model = Medewerker
    id_field = "uuid"

    def delete(self, *args, **kwargs):
        print("SCIM DELETE received with UUID:", self.id)
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

    @property
    def meta(self):
        created = getattr(self.obj, "created_at", None)
        updated = getattr(self.obj, "updated_at", None)
        return {
            "resourceType": self.resource_type,
            "created": created.isoformat() if created else None,
            "lastModified": updated.isoformat() if updated else None,
            "location": self.location,
        }

    def to_dict(self):
        logger.warning(
            "SCIM to_dict output: %s",
            json.dumps({"active": self.obj.actief, "type": str(type(self.obj.actief))}),
        )
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
        self.obj.medewerker_id = d.get("externalId", self.obj.medewerker_id)
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
        else:
            self.obj.emailadres = d.get("userName", self.obj.emailadres)

        phone_numbers = d.get("phoneNumbers", [])
        if phone_numbers:
            self.obj.telefoonnummer = phone_numbers[0].get("value", "")

        active = d.get("active")
        if isinstance(active, bool):
            self.obj.actief = active
        elif isinstance(active, str):
            self.obj.actief = active.strip().lower() == "true"
        elif active is None:
            pass  # leave self.obj.actief unchanged
        else:
            logger.warning(
                f"Unexpected type for 'active': {type(active)} — setting to False"
            )
            self.obj.actief = False

        self.obj.functie = d.get("functie", self.obj.functie)

        self.obj.save()
