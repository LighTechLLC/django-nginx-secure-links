import re

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

from nginx_secure_links import settings as app_settings


class Command(BaseCommand):
    help = 'Generates a sample of Nginx location basing on the settings'

    def handle(self, *args, **options):
        private_suffixes = []
        public_suffixes = []
        media_root = str(settings.MEDIA_ROOT).rstrip("/")
        media_location = settings.MEDIA_URL.replace(
            default_storage.not_hashable_prefix, ""
        ).rstrip("/")

        # prefixes preparing
        for prefix in app_settings.SECURE_LINK_PRIVATE_PREFIXES:
            private_suffixes.append(prefix.strip("/"))
        for prefix in app_settings.SECURE_LINK_PUBLIC_PREFIXES:
            public_suffixes.append(prefix.strip("/"))
        media_is_private = (
            len(public_suffixes) > 0 or len(private_suffixes) == 0
        )
        context = {
            'private_suffixes': private_suffixes,
            'public_suffixes': public_suffixes,
            'media_is_private': media_is_private,
            'media_location': media_location,
            'media_root': media_root,
            'token_field': app_settings.SECURE_LINK_TOKEN_FIELD,
            'expires_field': app_settings.SECURE_LINK_EXPIRES_FIELD,
            'secret': app_settings.SECURE_LINK_SECRET_KEY,
        }
        rendered_locations = render_to_string(
            'nginx_secure_links/locations.conf', context
        )
        rendered_locations = re.sub('\n\n+', '\n', rendered_locations).strip()
        self.stdout.write(rendered_locations)
