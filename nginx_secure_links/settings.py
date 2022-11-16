from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

SECURE_LINK_EXPIRATION_SECONDS = getattr(
    settings, 'SECURE_LINK_EXPIRATION_SECONDS', 60 * 60 * 24
)
SECURE_LINK_TIMEZONE = getattr(settings, 'SECURE_LINK_TIMEZONE', 'UTC')
SECURE_LINK_SECRET_KEY = getattr(settings, 'SECURE_LINK_SECRET_KEY')
SECURE_LINK_TOKEN_FIELD = getattr(settings, 'SECURE_LINK_TOKEN_FIELD', 'token')
SECURE_LINK_EXPIRES_FIELD = getattr(
    settings, 'SECURE_LINK_EXPIRES_FIELD', 'expires'
)
SECURE_LINK_PRIVATE_PREFIXES = getattr(
    settings, 'SECURE_LINK_PRIVATE_PREFIXES', []
)
SECURE_LINK_PUBLIC_PREFIXES = getattr(
    settings, 'SECURE_LINK_PUBLIC_PREFIXES', []
)
if (
    len(SECURE_LINK_PRIVATE_PREFIXES) > 0
    and len(SECURE_LINK_PUBLIC_PREFIXES) > 0
):
    raise ImproperlyConfigured(
        'Only SECURE_LINK_PRIVATE_PREFIXES or SECURE_LINK_PUBLIC_PREFIXES '
        'should be specified, not both'
    )
