from django.conf import settings

custom_settings = {
    "VERSION": settings.SCIM_API_VERSION,
    "SERVERS": [{"url": f"/medewerksers/api/v{settings.SCIM_API_MAJOR_VERSION}"}],
}
