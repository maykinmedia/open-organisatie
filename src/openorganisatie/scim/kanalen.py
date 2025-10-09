from openorganisatie.utils.kanaal import Kanaal

from .models.medewerker import Medewerker
from .models.user import User

KANAAL_IDENTITEIT = Kanaal(
    "users",
    main_resource=User,
    kenmerken=(
        "username",
        "username",
        "email",
    ),
    extra_kwargs={"scim_external_id": {"help_text": "Object id van de user"}},
)

KANAAL_ORGANISATIE = Kanaal(
    "medewerkers",
    main_resource=Medewerker,
    kenmerken=(
        "medewerker_id",
        "first_name",
        "email",
    ),
    extra_kwargs={"uuid": {"help_text": "uuid van de medewerker"}},
)
