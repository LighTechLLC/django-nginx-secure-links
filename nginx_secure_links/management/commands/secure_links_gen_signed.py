from django.conf import settings
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Generates pre-signed url by passing public url'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, default=1)
        parser.add_argument('--seconds', type=int, default=1)

    def handle(self, *args, **options):
        seconds = options.get(
            'seconds', settings.SECURE_LINK_EXPIRATION_SECONDS
        )
        url = default_storage.pre_sign_url(options['url'], seconds)
        self.stdout.write(url)
