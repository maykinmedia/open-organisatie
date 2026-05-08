from urllib.parse import urljoin

from django.urls import reverse
from django.utils import timezone

import structlog
from django_scim.adapters import SCIMGroup, SCIMUser
from notifications_api_common.viewsets import NotificationMixin
from psycopg.types.range import DateRange
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from reversion import create_revision, set_comment

from openorganisatie.identiteit.kanalen import KANAAL_IDENTITEIT
from openorganisatie.identiteit.models.relaties import UserGroup

from ..identiteit.api.serializers.user import UserSerializer
from .models.group import Group
from .models.user import User

logger = structlog.stdlib.get_logger(__name__)


class ReversionSCIMMixin:
    def save(self):
        with create_revision():
            result = super().save()

            try:
                comment_location = self.location
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

    def delete(self):
        logger.info("scim_group_deleted", group=self.id)

        # IMPORTANT: use SCIM ID field, NOT Django PK
        self.model.objects.filter(scim_external_id=self.id).delete()

    @property
    def members(self):
        memberships = UserGroup.objects.filter(group=self.obj)

        return [
            {
                "value": str(m.user.scim_external_id),
                "$ref": UserAdapter(m.user, request=self.request).location,
                "display": m.user.username,
                "startDate": m.periode.lower.isoformat()
                if m.periode and m.periode.lower
                else None,
                "endDate": m.periode.upper.isoformat()
                if m.periode and m.periode.upper
                else None,
            }
            for m in memberships.select_related("user")
        ]

    def handle_add(self, path, value, operation):
        if path.first_path != ("members", None, None):
            raise NotImplementedError

        members = value or []
        ids = [m.get("value") for m in members]

        users = User.objects.filter(scim_external_id__in=ids)
        if len(ids) != users.count():
            return

        today = timezone.now().date()

        for user in users:
            exists = UserGroup.objects.filter(
                user=user, group=self.obj, periode__upper_inf=True
            ).exists()

            if exists:
                continue

            UserGroup.objects.create(
                user=user,
                group=self.obj,
                periode=DateRange(lower=today, upper=None),
            )

        logger.info(
            "scim_group_members_added",
            team=str(self.obj.name),
            added_members=[str(u.scim_external_id) for u in users],
        )

    def handle_remove(self, path, value, operation):
        if path.first_path != ("members", None, None):
            raise NotImplementedError

        members = value or []
        ids = [m.get("value") for m in members]

        users = User.objects.filter(scim_external_id__in=ids)
        today = timezone.now().date()

        for user in users:
            membership = (
                UserGroup.objects.filter(
                    user=user,
                    group=self.obj,
                    periode__contains=today,
                )
                .order_by("-wijzigingsdatum")
                .first()
            )

            if not membership:
                continue

            membership.periode = DateRange(
                lower=membership.periode.lower,
                upper=today,
            )
            membership.save(update_fields=["periode"])
