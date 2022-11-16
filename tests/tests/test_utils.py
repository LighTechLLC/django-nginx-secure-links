from nginx_secure_links import utils


def test_result_type():
    value = utils.gen_hash('/media/report.pdf', 100, 'secret')
    assert isinstance(value, str)


def test_sample_rows():
    """
    Tests hardcoded urls by using utils.gen_hash function.
    It tries to compare python has algorithm with openssl way.

    Bash sample1:
         echo -n '100/media/sample1.pdf secret_xyz' |
           openssl md5 -binary |
           openssl base64 |
           tr +/ -_ | tr -d =
         echo -n '100/media/sample2.pdf secret_xyz' |
           openssl md5 -binary |
           openssl base64 |
           tr +/ -_ | tr -d =
         echo -n '100/media/extra_sample.pdf secret_xyz' |
           openssl md5 -binary |
           openssl base64 |
           tr +/ -_ | tr -d =
         echo -n '100/media_extra/extra_sample secret_xyz' |
           openssl md5 -binary |
           openssl base64 |
           tr +/ -_ | tr -d =
    """
    secret_key = 'secret_xyz'
    timestamp_value = 100
    samples = {
        '/media/sample1.pdf': 'Cwl-gVMjo1qYm3D5TZzuRA',
        '/media/sample2.pdf': '06Asv1u7v4X7oG3LdTlP8Q',
        '/media/extra_sample.pdf': 'CePxq3rkgBfoMSfccBBSlA',
        '/media_extra/extra_sample2.pdf': 'deBir1drX8MDqFMLHnMawA',
    }
    for url, result in samples.items():
        token = utils.gen_hash(
            url=url,
            expires_timestamp=timestamp_value,
            secret_key=secret_key,
        )
        assert token == result
