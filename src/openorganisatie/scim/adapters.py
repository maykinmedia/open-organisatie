from django_scim.adapters import SCIMUser

from .models.medewerker import Medewerker


class MedewerkerAdapter(SCIMUser):
    model = Medewerker
    id_field = "username"
    url_name = "scim:user-detail"

    def delete(self, *args, **kwargs):
        self.model.objects.filter(**{self.id_field: self.id}).delete()

    @property
    def groups(self):
        return []

    @property
    def phone_numbers(self):
        if self.obj.phone_number:
            return [{"value": self.obj.phone_number, "type": "work"}]
        return []

    def to_dict(self):
        d = super().to_dict()

        d.update(
            {
                "userName": str(self.obj.username),
                "phoneNumbers": self.phone_numbers,
                "jobTitle": self.obj.job_title,
            }
        )

        return d

    def from_dict(self, d):
        super().from_dict(d)

        name = d.get("name", {})
        if name:
            self.obj.first_name = name.get("givenName", "")
            self.obj.last_name = name.get("familyName", "")
        else:
            display_name = d.get("displayName", "")
            if display_name:
                parts = display_name.split(" ", 1)
                self.obj.first_name = parts[0]
                if len(parts) > 1:
                    self.obj.last_name = parts[1]
                else:
                    self.obj.last_name = ""

        phone_numbers = d.get("phoneNumbers", [])
        if phone_numbers:
            self.obj.phone_number = phone_numbers[0].get("value", "")

        job_title = d.get("jobTitle")
        if job_title is not None:
            self.obj.job_title = job_title

        self.obj.save()

    def handle_operations(self, operations):
        for op in operations:
            operation = op["op"].lower()
            path = op.get("path", "").lower()
            value = op.get("value")

            if path == "active" and isinstance(value, str):
                val = value.strip().lower()
                if val in ("true", "false"):
                    value = val == "true"

            if operation in ("replace", "add"):
                if path == "active":
                    self.obj.is_active = bool(value)
                elif path == "username":
                    self.obj.username = value
                elif path == "phonenumbers":
                    if isinstance(value, list) and value:
                        self.obj.phone_number = value[0].get("value", "")
                elif path == "jobtitle":
                    self.obj.job_title = value
            elif operation == "remove":
                if path == "username":
                    self.obj.username = ""

        self.obj.save()
