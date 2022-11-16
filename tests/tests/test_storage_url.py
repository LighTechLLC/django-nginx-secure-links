from urllib.parse import urlparse, parse_qs

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
