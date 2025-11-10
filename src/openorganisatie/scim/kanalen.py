from notifications_api_common.kanalen import Kanaal

from .models.medewerker import Medewerker
from .models.user import User

KANAAL_IDENTITEIT = Kanaal(
    "users",
    main_resource=User,
    kenmerken=(
        "scim_external_id",
        "username",
        "email",
    ),
)

KANAAL_ORGANISATIE = Kanaal(
    "medewerkers",
    main_resource=Medewerker,
    kenmerken=(
        "uuid",
        "medewerker_id",
        "voornaam",
        "achternaam",
        "emailadres",
    ),
)
