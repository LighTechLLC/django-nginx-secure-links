import datetime
from unittest.mock import Mock

import pytest
from django.core.files.storage import default_storage

import nginx_secure_links.utils
from nginx_secure_links.storages import FileStorage


@pytest.fixture()
def default_media_storage():
    return default_storage


@pytest.fixture()
def storage_settings(settings):
    settings.SECURE_LINK_EXPIRATION_SECONDS = 10
    settings.SECURE_LINK_SECRET_KEY = 'secret'
    settings.SECURE_LINK_TOKEN_FIELD = 'custom_token'
    settings.SECURE_LINK_EXPIRES_FIELD = 'custom_expires'
    settings.SECURE_LINK_PRIVATE_PREFIXES = ['private/']
    settings.SECURE_LINK_PUBLIC_PREFIXES = []


@pytest.fixture()
def dt_static_value():
    return datetime.datetime(2020, 9, 4, 10, 10, 10)


@pytest.fixture(autouse=True)
def mocked_datetime(dt_static_value, monkeypatch):
    tz_now_value = datetime.datetime(2020, 9, 4, 10, 10, 10)

    class custom_datetime:
        @classmethod
        def utcnow(cls):
            return tz_now_value

        @classmethod
        def now(cls, tz=None):
            return tz_now_value

    monkeypatch.setattr(datetime, 'datetime', custom_datetime)


@pytest.fixture()
def storage_params():
    return {
        'nginx_secret_key': 'secret_xyz',
        'expires_field_name': 'expires_sample',
        'token_field_name': 'token_sample',
        'private_prefixes': ['private', 'personal', 'documents'],
        'public_prefixes': ['public', 'shared'],
        'expires_seconds': 100,
    }


@pytest.fixture()
def storage(storage_params):
    return FileStorage(**storage_params)


@pytest.fixture()
def storage_params_partially_private():
    return {
        'nginx_secret_key': 'secret_xyz',
        'expires_field_name': 'expires_sample',
        'token_field_name': 'token_sample',
        'private_prefixes': ['private', 'personal', 'documents'],
        'public_prefixes': [],
        'expires_seconds': 100,
    }


@pytest.fixture()
def storage_params_partially_public():
    return {
        'nginx_secret_key': 'secret_xyz',
        'expires_field_name': 'expires_sample',
        'token_field_name': 'token_sample',
        'private_prefixes': [],
        'public_prefixes': ['shared', 'icons'],
        'expires_seconds': 100,
    }


@pytest.fixture()
def storage_params_full_private():
    return {
        'nginx_secret_key': 'secret_xyz',
        'expires_field_name': 'expires_sample',
        'token_field_name': 'token_sample',
        'private_prefixes': [],
        'public_prefixes': [],
        'expires_seconds': 100,
    }


@pytest.fixture()
def partially_private_storage(storage_params_partially_private):
    return FileStorage(**storage_params_partially_private)


@pytest.fixture()
def partially_public_storage(storage_params_partially_public):
    return FileStorage(**storage_params_partially_public)


@pytest.fixture()
def private_storage(storage_params_full_private):
    return FileStorage(**storage_params_full_private)


@pytest.fixture()
def mock_utils_obj():
    return Mock()


@pytest.fixture()
def mocked_utils_gen_hash(monkeypatch, mock_utils_obj):
    monkeypatch.setattr(nginx_secure_links.utils, 'gen_hash', mock_utils_obj)
