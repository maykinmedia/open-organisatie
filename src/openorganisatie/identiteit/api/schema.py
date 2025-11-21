from django.conf import settings

from notifications_api_common.utils import notification_documentation

from ..kanalen import KANAAL_IDENTITEIT

description = f"""
Een API voor Identiteiten.

De Identiteiten API heeft 2 endpoints `group` en `users`.
Beide endpoints zijn **read-only**, wat betekent dat ze alleen gegevens kunnen ophalen en niet wijzigen.

Gegevens kunnen wel toegevoegd of gewijzigd worden via **SCIM**.

### Notificaties

{notification_documentation(KANAAL_IDENTITEIT)}

"""

custom_settings = {
    "VERSION": settings.API_VERSION,
    "DESCRIPTION": description,
    "SERVERS": [{"url": f"/identiteit/api/v{settings.SCIM_API_MAJOR_VERSION}"}],
}
