from django.conf import settings

custom_settings = {
    "VERSION": settings.API_VERSION,
    "SERVERS": [{"url": f"/medewerkers/api/v{settings.SCIM_API_MAJOR_VERSION}"}],
}
