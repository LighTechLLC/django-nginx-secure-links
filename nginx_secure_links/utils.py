import base64
import hashlib
from datetime import timedelta, datetime


def gen_hash(url: str, expires_timestamp: int, secret_key: str) -> str:
    raw_value = '{expires_timestamp}{url} {secret_key}'.format(
        expires_timestamp=expires_timestamp, url=url, secret_key=secret_key
    )
    md5_hash = hashlib.md5(raw_value.encode('utf-8')).digest()
    base64_token = (
        base64.urlsafe_b64encode(md5_hash)
        .decode('utf-8')
        .replace('=', '')
        .replace('/', '')
    )
    return base64_token


def gen_expires(dt: datetime, seconds: int) -> int:
    expires_timedelta = timedelta(seconds=seconds)
    expires_at = dt + expires_timedelta
    timestamp = int(expires_at.timestamp())
    return timestamp
