from urllib.parse import urljoin

from django.urls import reverse

import structlog
from django_scim.adapters import SCIMGroup, SCIMUser
from notifications_api_common.viewsets import NotificationMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from reversion import create_revision, set_comment

from openorganisatie.identiteit.kanalen import KANAAL_IDENTITEIT

from ..identiteit.api.serializers.user import UserSerializer
from .models.group import Group
from .models.user import User

logger = structlog.stdlib.get_logger(__name__)


class ReversionSCIMMixin:
    def save(self):
        with create_revision():
            result = super().save()  # type: ignore[reportAttributeAccessIssue]

            try:
                comment_location = self.location  # type: ignore[attr-defined]
                set_comment(f"Updated via SCIM - {comment_location}")
            except Exception:
                set_comment("Updated via SCIM")

        return result


class UserAdapter(ReversionSCIMMixin, NotificationMixin, SCIMUser):
    model = User
    queryset = User.objects.all()
    id_field = "scim_external_id"
    url_name = "scim:user-detail"
    notifications_kanaal = KANAAL_IDENTITEIT
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.queryset

    @classmethod
    def get_extra_actions(cls):
        return []

    @property
    def action(self):
        return "create" if getattr(self, "_is_create", False) else "update"

    def delete(self, *args, **kwargs):
        logger.info("scim_user_deleted", username=self.id)
        self.model.objects.filter(**{self.id_field: self.id}).delete()

    @property
    def id(self):
        return str(self.obj.scim_external_id)

    @property
    def path(self):
        return reverse(self.url_name, kwargs={"uuid": str(self.obj.scim_external_id)})

    @property
    def location(self):
        base_url = self.request.build_absolute_uri("/scim/v2/")
        return urljoin(base_url, self.path)

    @property
    def groups(self):
        return [
            {
                "value": str(team.scim_external_id),
                "$ref": GroupAdapter(team, request=self.request).location,
                "display": team.name,
            }
            for team in self.obj.groups.all()
        ]

    def to_dict(self):
        if not hasattr(self.obj, "first_name"):
            self.obj.first_name = ""
        if not hasattr(self.obj, "last_name"):
            self.obj.last_name = ""

        d = super().to_dict()

        d.update(
            {
                "scimExternalId": str(self.obj.scim_external_id),
                "userName": str(self.obj.username),
                "url": self.location,
            }
        )

        return d

    def from_dict(self, d):
        super().from_dict(d)

        enterprise_ext = d.get(
            "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User", {}
        )
        if enterprise_ext:
            self.obj.employee_number = enterprise_ext.get("employeeNumber")

        logger.info(
            "add_scim_user",
            username=str(self.obj.username),
        )

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
            elif operation == "remove":
                if path == "username":
                    self.obj.username = ""

        self.save()

        logger.info(
            "update_scim_user",
            username=str(self.obj.username),
            operations=operations,
        )

    def save(self):
        self._is_create = self.obj.pk is None
        super().save()

        self.obj.koppel_medewerker()

        try:
            serializer = self.serializer_class(
                instance=self.obj,
                context={"request": self.request},
            )
            response = Response(
                serializer.data,
                status=HTTP_201_CREATED if self._is_create else HTTP_200_OK,
            )
            data = response.data
            data["url"] = self.location

            self.notify(
                status_code=response.status_code,
                data=data,
                instance=self.obj,
            )
            logger.info(
                "scim_user_notification_sent",
                username=str(self.obj.username),
                action=self.action,
            )
        except Exception as e:
            logger.warning(
                "scim_user_notification_failed",
                username=str(self.obj.username),
                error=str(e),
            )


class GroupAdapter(ReversionSCIMMixin, SCIMGroup):
    model = Group
    url_name = "scim:group-detail"
    id_field = "scim_external_id"

    @property
    def members(self):
        return [
            {
                "value": str(user.username),
                "$ref": UserAdapter(user, request=self.request).location,
                "display": f"{user.username}".strip(),
            }
            for user in self.obj.user_set.all()
        ]

    def handle_add(self, path, value, operation):
        if path.first_path == ("members", None, None):
            members = value or []
            ids = [member.get("value") for member in members]

            users = User.objects.filter(scim_external_id__in=ids)
            if len(ids) != users.count():
                return

            for user in users:
                self.obj.user_set.add(user)

            logger.info(
                "scim_group_members_added",
                team=str(self.obj.name),
                team_id=str(self.obj.scim_external_id),
                added_members=[str(user.scim_external_id) for user in users],
            )
        else:
            raise NotImplementedError

    def handle_remove(self, path, value, operation):
        if path.first_path == ("members", None, None):
            members = value or []

            ids = [member.get("value") for member in members]

            users = User.objects.filter(scim_external_id__in=ids)
            if len(ids) != users.count():
                return

            for user in users:
                self.obj.user_set.remove(user)

            logger.info(
                "scim_group_members_removed",
                team=str(self.obj.name),
                team_id=str(self.obj.scim_external_id),
                removed_members=[str(user.scim_external_id) for user in users],
            )
        else:
            raise NotImplementedError
