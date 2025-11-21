from django.conf import settings
from django.utils.translation import gettext_lazy as _

from notifications_api_common.utils import notification_documentation

from ..kanalen import KANAAL_ORGANISATIE

description = _(f"""
Een API voor Organisaties.

De Organisatie API heeft de volgende endpoints `medewerkers`, `teams`, `vestigingen`, `organisatorische eenheden`, `functies`, `functietypes`.

### Notificaties

{notification_documentation(KANAAL_ORGANISATIE)}
""")
custom_settings = {
    "TITLE": "Organisatie API",
    "VERSION": settings.ORGANISATIE_API_VERSION,
    "DESCRIPTION": description,
    "SERVERS": [{"url": f"/organisatie/api/v{settings.API_VERSION}"}],
}
