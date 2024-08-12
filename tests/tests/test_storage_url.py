from urllib.parse import parse_qs, urlparse

import pytest

from nginx_secure_links import utils


def test_openssl_hashed_string_similarity(
    dt_static_value,
    storage_params_partially_private,
    partially_private_storage,
):
    # 1599214310/media/private/sample1.pdf secret_xyz
    sample_path = 'private/sample1.pdf'
    sample_token = 'GdxTxfNK92Grtg-hD7CH6g'

    expires_timestamp = str(
        utils.gen_expires(
            dt_static_value,
            seconds=storage_params_partially_private['expires_seconds'],
        )
    )

    url: str = partially_private_storage.url(sample_path)
    o = urlparse(url)
    params = parse_qs(o.query)

    # check path
    expected_path = '{media_url}{filename}'.format(
        media_url=partially_private_storage.base_url,
        filename=sample_path,
    )
    assert o.path == expected_path

    token_field_name = storage_params_partially_private['token_field_name']
    expires_field_name = storage_params_partially_private['expires_field_name']
    assert token_field_name in params
    assert expires_field_name in params
    assert params[expires_field_name][0] == expires_timestamp
    assert params[token_field_name][0] == sample_token


def test_openssl_hashed_string_similarity_with_custom_lifetime(
    dt_static_value,
    storage_params_partially_private,
    partially_private_storage,
):
    # 1599337666/media/private/sample1.pdf secret_xyz
    sample_path = 'private/sample1.pdf'
    sample_token = '4E1lyDQkWbenekEqdZpClQ'
    lifetime = 123456

    expires_timestamp = str(
        utils.gen_expires(
            dt_static_value,
            seconds=lifetime,
        )
    )

    url: str = partially_private_storage.url(sample_path, lifetime=lifetime)
    o = urlparse(url)
    params = parse_qs(o.query)

    # check path
    expected_path = '{media_url}{filename}'.format(
        media_url=partially_private_storage.base_url,
        filename=sample_path,
    )
    assert o.path == expected_path

    token_field_name = storage_params_partially_private['token_field_name']
    expires_field_name = storage_params_partially_private['expires_field_name']
    assert token_field_name in params
    assert expires_field_name in params
    assert params[expires_field_name][0] == expires_timestamp
    assert params[token_field_name][0] == sample_token


def test_openssl_hashed_string_similarity_with_unlimited_lifetime(
    dt_static_value,
    storage_params_partially_private,
    partially_private_storage,
):
    # /media/private/sample1.pdf secret_xyz
    sample_path = 'private/sample1.pdf'
    sample_token = 'P1LB2On7XTx5j4pZmYQaRw'
    lifetime = 0

    url: str = partially_private_storage.url(sample_path, lifetime=lifetime)
    o = urlparse(url)
    params = parse_qs(o.query)

    # check path
    expected_path = '{media_url}{filename}'.format(
        media_url=partially_private_storage.base_url,
        filename=sample_path,
    )
    assert o.path == expected_path

    token_field_name = storage_params_partially_private['token_field_name']
    expires_field_name = storage_params_partially_private['expires_field_name']
    assert token_field_name in params
    assert expires_field_name not in params
    assert params[token_field_name][0] == sample_token


def test_openssl_hashed_string_similarity_with_negative_lifetime(
    partially_private_storage,
):
    sample_path = 'private/sample1.pdf'
    lifetime = -1

    with pytest.raises(ValueError) as e:
        partially_private_storage.url(sample_path, lifetime=lifetime)
    assert str(e.value) == 'The value of `lifetime` should not be negative.'
