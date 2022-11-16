from nginx_secure_links import utils


def test_openssl_hashed_string_similarity(
    dt_static_value,
    storage_params_partially_private,
    partially_private_storage,
):
    """Comparing `utils.gen_hash` result with a token made in bash"""
    url = '/media/private/sample1.pdf'
    expires = 1599214310
    secret = 'secret_xyz'
    # Example: 1599214310/media/private/sample1.pdf secret_xyz
    sample_token = 'GdxTxfNK92Grtg-hD7CH6g'

    token = utils.gen_hash(
        url=url, expires_timestamp=expires, secret_key=secret
    )
    assert token == sample_token
