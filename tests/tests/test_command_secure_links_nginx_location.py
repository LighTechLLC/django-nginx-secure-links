from io import StringIO

from django.core.management import call_command


def test_call_command(settings):
    out = StringIO()
    call_command(
        'secure_links_nginx_location',
        stdout=out,
        stderr=StringIO(),
    )
    result_str = out.getvalue().strip()
    args_raw = 'secure_link $arg_{token_field},$arg_{expires_field};'
    link_pattern_raw = 'secure_link_md5 "$secure_link_expires$uri {secret}";'
    r1 = args_raw.format(
        token_field=settings.SECURE_LINK_TOKEN_FIELD,
        expires_field=settings.SECURE_LINK_EXPIRES_FIELD,
    )
    r2 = link_pattern_raw.format(secret=settings.SECURE_LINK_SECRET_KEY)
    assert r1 in result_str
    assert r2 in result_str
