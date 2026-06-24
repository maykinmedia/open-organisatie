from notifications_api_common.kanalen import Kanaal

from .models.medewerker import Medewerker

KANAAL_ORGANISATIE = Kanaal(
    "medewerkers",
    main_resource=Medewerker,  # type: ignore[attr-defined]
    kenmerken=(
        "uuid",
        "medewerker_id",
        "voornaam",
        "achternaam",
        "emailadres",
    ),
)
