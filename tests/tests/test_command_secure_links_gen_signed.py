from io import StringIO

from django.core.files.storage import default_storage
from django.core.management import call_command


def test_call_command(settings):
    out = StringIO()
    url = '/media/private/report.pdf'
    seconds = 90
    call_command(
        'secure_links_gen_signed',
        url,
        '--seconds',
        seconds,
        stdout=out,
        stderr=StringIO(),
    )
    command_url = out.getvalue().strip()
    expected_url = default_storage.pre_sign_url(url, seconds)
    assert command_url == expected_url
