from django.conf import settings
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand

from nginx_secure_links import settings as app_settings


class Command(BaseCommand):
    help = 'Generates a sample of Nginx location basing on the settings'

    def handle(self, *args, **options):
        pattern = """
        location %(media_url)s {
            secure_link $arg_%(token_field)s,$arg_%(expires_field)s;
            secure_link_md5 "$secure_link_expires$uri %(secret)s";

            if ($secure_link = "") {
                return 403;
            }

            if ($secure_link = "0") {
                return 410;
            }

            alias %(media_root)s;
        }\n"""
        media_location_path = settings.MEDIA_URL.replace(
            default_storage.not_hashable_prefix, ''
        )
        text = pattern % dict(
            token_field=app_settings.SECURE_LINK_TOKEN_FIELD,
            expires_field=app_settings.SECURE_LINK_EXPIRES_FIELD,
            secret=app_settings.SECURE_LINK_SECRET_KEY,
            media_root=settings.MEDIA_ROOT,
            media_url=media_location_path,
        )
        self.stdout.write(text)
