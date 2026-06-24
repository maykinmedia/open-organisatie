from notifications_api_common.kanalen import Kanaal

from .models.user import User

KANAAL_IDENTITEIT = Kanaal(
    "users",
    main_resource=User,  # type: ignore[attr-defined]
    kenmerken=(
        "scim_external_id",
        "username",
        "email",
    ),
)
