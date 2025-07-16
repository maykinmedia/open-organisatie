import xml.etree.ElementTree as ET

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

    @property
    def app_role_assignments(self):
        """SCIM appRoleAssignments mapping"""
        if hasattr(self.obj, "get_app_role_assignments"):
            return self.obj.get_app_role_assignments()
        return []

    def to_dict(self):
        d = super().to_dict()

        d.update(
            {
                "userName": str(self.obj.username),
                "phoneNumbers": self.phone_numbers,
                "jobTitle": self.obj.job_title,
                "appRoleAssignments": self.app_role_assignments,
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

        roles_raw = d.get("roles", [])
        role_values = []
        role_displays = []

        if isinstance(roles_raw, list):
            for role in roles_raw:
                display_xml = role.get("display")
                if display_xml:
                    display_xml = display_xml.strip()
                    if display_xml.startswith("<?xml"):
                        try:
                            root = ET.fromstring(display_xml)

                            # Extract <Value> elements text using wildcard for namespace
                            for val_elem in root.findall(".//{*}Value"):
                                text = val_elem.text
                                if text is None:
                                    continue  # skip empty values
                                text = text.strip()
                                if text.startswith("<?xml"):
                                    continue
                                role_values.append(text)

                            # Extract <TypeName> elements text using wildcard for namespace
                            for name_elem in root.findall(".//{*}Name"):
                                if name_elem.text:
                                    print("namennnnn", name_elem.text)
                                    role_displays.append(name_elem.text.strip())

                            # Extract <Type> elements text using wildcard for namespace
                            for type_elem in root.findall(".//{*}Type"):
                                if (
                                    type_elem.text
                                    and type_elem.text not in role_displays
                                ):
                                    role_displays.append(type_elem.text)

                        except ET.ParseError as e:
                            print("Failed to parse roles XML:", e)
                            # Optionally, you can append raw display XML or skip
                    else:
                        # Not XML, treat as plain role string
                        return
        else:
            print("roles_raw is not a list as expected")

        print("Extracted role values:", role_values)
        print("Extracted role displays:", role_displays)

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
                elif path == "roles":
                    if isinstance(value, list):
                        for role in value:
                            if (
                                isinstance(role, dict)
                                and role.get("primary")
                                and role.get("display")
                            ):
                                self.obj.primary_role_display = role["display"]
            elif operation == "remove":
                if path == "username":
                    self.obj.username = ""

        self.obj.save()
