import pytest
from django.core.exceptions import ImproperlyConfigured

from nginx_secure_links.storages import FileStorage


def test_custom_expires_seconds_property():
    seconds = 1_234_567
    storage = FileStorage(expires_seconds=seconds)
    assert storage.expires_seconds == seconds


def test_expires_seconds_default_property(settings):
    """
    `expires_seconds` value should be equal to
     settings.SECURE_LINK_EXPIRATION_SECONDS when no custom value specified
    """
    storage = FileStorage()
    assert storage.expires_seconds == settings.SECURE_LINK_EXPIRATION_SECONDS


def test_custom_nginx_secret_key_property():
    """
    Custom secret key value should be returned in nginx_secret_key
     cached_property
    """
    secret = 'secret_raw'
    storage = FileStorage(nginx_secret_key=secret)
    assert storage.nginx_secret_key == secret


def test_default_nginx_secret_key_property(settings):
    """
    `nginx_secret_key` value should be equal to settings.SECURE_LINK_SECRET_KEY
     when no custom value specified
    """
    storage = FileStorage()
    assert storage.nginx_secret_key == settings.SECURE_LINK_SECRET_KEY


def test_custom_token_field_name_property():
    """
    Custom token field name should be returned in token_field_name
     cached_property
    """
    name = 'token_sample'
    storage = FileStorage(token_field_name=name)
    assert storage.token_field_name == name


def test_default_token_field_name_property(settings):
    """
    `token_field_name` value should be equal to
     settings.SECURE_LINK_TOKEN_FIELD when no custom value specified
    """
    storage = FileStorage()
    assert storage.token_field_name == settings.SECURE_LINK_TOKEN_FIELD


def test_custom_expires_field_name_property(settings):
    """
    Custom expires field name should be returned in `expires_field_name`
     cached_property
    """
    name = 'expires_sample'
    storage = FileStorage(expires_field_name=name)
    assert storage.expires_field_name == name


def test_default_expires_field_name_property(settings):
    """
    `expires_field_name` value should be equal to
     settings.SECURE_LINK_EXPIRES_FIELD when no custom value specified
    """
    storage = FileStorage()
    assert storage.expires_field_name == settings.SECURE_LINK_EXPIRES_FIELD


def test_custom_private_prefixes_property(settings):
    """
    Custom private prefixes should be returned in `private_prefixes`
     cached_property
    """
    prefixes = ['x', 'y', 'z']
    storage = FileStorage(private_prefixes=prefixes, public_prefixes=[])
    assert storage.private_prefixes == prefixes


def test_default_private_prefixes_property(settings):
    """
    `private_prefixes` value should be equal to
     settings.SECURE_LINK_PRIVATE_PREFIXES when no custom value specified
    """
    storage = FileStorage()
    assert storage.private_prefixes == settings.SECURE_LINK_PRIVATE_PREFIXES


def test_custom_public_prefixes_property(settings):
    """
    Custom public prefixes should be returned in `public_prefixes`
     cached_property
    """
    prefixes = ['x', 'y', 'z']
    storage = FileStorage(private_prefixes=[], public_prefixes=prefixes)
    assert storage.public_prefixes == prefixes


def test_default_public_prefixes_property(settings):
    """
    `public_prefixes` value should be equal to
     settings.SECURE_LINK_PUBLIC_PREFIXES when no custom value specified
    """
    storage = FileStorage()
    assert storage.public_prefixes == settings.SECURE_LINK_PUBLIC_PREFIXES


def test_prefixes_property_when_public_specified(settings):
    """
    `prefixes` value should be equal to `public_prefixes` when
     public_prefixes specified
    """
    public_prefixes = ['x', 'y', 'z']
    private_prefixes = []
    storage = FileStorage(
        private_prefixes=private_prefixes, public_prefixes=public_prefixes
    )
    assert storage.prefixes == public_prefixes


def test_prefixes_property_when_private_specified(settings):
    """
    `prefixes` value should be equal to `private_prefixes` when
     private_prefixes specified
    """
    public_prefixes = []
    private_prefixes = ['x', 'y', 'z']
    storage = FileStorage(
        private_prefixes=private_prefixes, public_prefixes=public_prefixes
    )
    assert storage.prefixes == private_prefixes


def test_prefixes_property_when_both_empty_specified(settings):
    """
    `prefixes` value should be equal to `[]` when no private_prefixes,
     no public_prefixes specified
    """
    public_prefixes = []
    private_prefixes = []
    storage = FileStorage(
        private_prefixes=private_prefixes, public_prefixes=public_prefixes
    )
    assert storage.prefixes == []


def test_prefixes_property_when_both_specified(settings):
    """
    ImproperlyConfigured should be raised when both
     private_prefixes and public_prefixes specified
    """
    public_prefixes = ['x']
    private_prefixes = ['y']
    storage = FileStorage(
        private_prefixes=private_prefixes, public_prefixes=public_prefixes
    )
    with pytest.raises(ImproperlyConfigured):
        storage.prefixes


def test_not_hashable_prefix_property_on_path_only(settings):
    """
    not_hashable_prefix should be equal to "" when path only specified,
     full path should be used in hashing algorithm
    """
    path = '/media-prefix/'
    storage = FileStorage(base_url=path)
    assert storage.not_hashable_prefix == ''


def test_not_hashable_prefix_property_on_full_http_url(settings):
    """
    not_hashable_prefix should be equal to "http://domain" when
     full url specified, only path should be used in hashing algorithm.
    """
    full_prefix = 'http://example.com'
    path = f'{full_prefix}/media-prefix/'
    storage = FileStorage(base_url=path)
    assert storage.not_hashable_prefix == full_prefix


def test_not_hashable_prefix_property_on_full_https_url(settings):
    """
    not_hashable_prefix should be equal to "https://domain" when
     full url specified, only path should be used in hashing algorithm.
    """
    full_prefix = 'https://example.com'
    path = f'{full_prefix}/media-prefix/'
    storage = FileStorage(base_url=path)
    assert storage.not_hashable_prefix == full_prefix


def test_prefix_predicate_property_on_private_prefixes(settings):
    """
    When private prefixes specified, prefix_predicate should check
    when result of comparison "path in private_prefixes" equals True.
    Cases:
     - prefix_predicate((path in prefix) is True) => True
     - prefix_predicate((path in prefix) is False) => False
    """
    private_prefixes = ['x']
    public_prefixes = []
    storage = FileStorage(
        private_prefixes=private_prefixes, public_prefixes=public_prefixes
    )
    assert storage.prefix_predicate(True)
    assert not storage.prefix_predicate(False)


def test_prefix_predicate_property_on_public_prefixes(settings):
    """
    When public prefixes specified, prefix_predicate should check
    when result of comparison "path in public_prefixes" equals False.
    Cases:
     - prefix_predicate((path in prefix) is True) => False
     - prefix_predicate((path in prefix) is False) => True
    """
    private_prefixes = []
    public_prefixes = ['x']
    storage = FileStorage(
        private_prefixes=private_prefixes, public_prefixes=public_prefixes
    )
    assert storage.prefix_predicate(False)


def test_prefix_predicate_property_on_empty_prefixes(settings):
    private_prefixes = []
    public_prefixes = []
    storage = FileStorage(
        private_prefixes=private_prefixes, public_prefixes=public_prefixes
    )
    assert storage.prefix_predicate(True)
    assert storage.prefix_predicate(False)
