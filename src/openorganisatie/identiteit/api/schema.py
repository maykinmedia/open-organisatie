from django.conf import settings

custom_settings = {
    "VERSION": settings.API_VERSION,
    "SERVERS": [{"url": f"/identiteit/api/v{settings.SCIM_API_MAJOR_VERSION}"}],
}
