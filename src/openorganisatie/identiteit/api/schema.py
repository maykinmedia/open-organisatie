from django.conf import settings
from django.utils.translation import gettext_lazy as _

from notifications_api_common.utils import notification_documentation

from ..kanalen import KANAAL_IDENTITEIT

description = _(f"""
Een API voor Identiteiten.

De Identiteiten API heeft 2 endpoints `group` en `users`.
Beide endpoints zijn **read-only**, wat betekent dat ze alleen gegevens kunnen ophalen en niet wijzigen.

Gegevens kunnen wel toegevoegd of gewijzigd worden via **SCIM**.

### Notificaties

{notification_documentation(KANAAL_IDENTITEIT)}

""")

custom_settings = {
    "TITLE": "Identiteit API",
    "VERSION": settings.IDENTITEIT_API_VERSION,
    "DESCRIPTION": description,
    "SERVERS": [{"url": f"/identiteit/api/v{settings.API_VERSION}"}],
}
