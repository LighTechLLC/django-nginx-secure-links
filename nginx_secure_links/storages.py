import datetime
import operator
import re
import urllib.parse
from urllib.parse import urlparse

from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import FileSystemStorage
from django.utils.functional import cached_property

from nginx_secure_links import settings as app_settings
from nginx_secure_links import utils


class FileStorage(FileSystemStorage):
    def __init__(
        self,
        *args,
        expires_seconds=None,
        nginx_secret_key=None,
        token_field_name=None,
        expires_field_name=None,
        private_prefixes=None,
        public_prefixes=None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        # secure links attributes
        self._expires_seconds = expires_seconds
        self._nginx_secret_key = nginx_secret_key
        self._token_field_name = token_field_name
        self._expires_field_name = expires_field_name
        self._private_prefixes = private_prefixes
        self._public_prefixes = public_prefixes

    @cached_property
    def expires_seconds(self) -> int:
        return self._value_or_setting(
            self._expires_seconds, app_settings.SECURE_LINK_EXPIRATION_SECONDS
        )

    @cached_property
    def nginx_secret_key(self) -> str:
        return self._value_or_setting(
            self._nginx_secret_key,
            app_settings.SECURE_LINK_SECRET_KEY,
        )

    @cached_property
    def token_field_name(self) -> str:
        return self._value_or_setting(
            self._token_field_name,
            app_settings.SECURE_LINK_TOKEN_FIELD,
        )

    @cached_property
    def expires_field_name(self) -> str:
        return self._value_or_setting(
            self._expires_field_name,
            app_settings.SECURE_LINK_EXPIRES_FIELD,
        )

    @cached_property
    def private_prefixes(self) -> list:
        return self._value_or_setting(
            self._private_prefixes,
            app_settings.SECURE_LINK_PRIVATE_PREFIXES,
        )

    @cached_property
    def public_prefixes(self) -> list:
        return self._value_or_setting(
            self._public_prefixes,
            app_settings.SECURE_LINK_PUBLIC_PREFIXES,
        )

    @cached_property
    def prefixes(self) -> list:
        if len(self.private_prefixes) > 0 and len(self.public_prefixes) > 0:
            raise ImproperlyConfigured

        return self.private_prefixes or self.public_prefixes or []

    @cached_property
    def not_hashable_prefix(self) -> str:
        """
        When `base_url` contains schema://domain:port/media/, only
        url path should be hashed.
        The method helps to calculate which prefix should not be hashed for
        further logic.
        """
        schema_prefix = r'^http(s)?://'
        if re.match(schema_prefix, self.base_url, re.I):
            o = urlparse(self.base_url)
            path_start_index = o.geturl().index(o.path)
            return self.base_url[:path_start_index]
        return ''

    @cached_property
    def prefix_predicate(self) -> callable:
        """
        Build an operator function which should be applied on the condition
         like "path in prefixes" inside `_is_secure_path(...)`.
        Since we use `self.prefixes` as a single property which optionally
        has private or public prefixes as a result (not both),
        we need to have a predicate for "path in self.prefixes" condition.
        The predicate is being used as a check "if path should be hashed".

        Cases:
         - private_prefixes specified:
             prefix in private_prefixes- should be hashed (True)
         - public_prefixes specified:
             prefix in public_prefixes- should not be hashed (False)
         - private_prefixes and public_prefixes are equal to "[]":
             should be always hashed, regardless of the condition result (True)
        """
        if len(self.private_prefixes) > 0:
            return operator.truth
        elif len(self.public_prefixes) > 0:
            return operator.not_
        return lambda x: True

    def _is_secure_path(self, url: str) -> bool:
        """Checks if the `url` should be hashed"""
        # shortcut: should not be iterating because of all urls will be private
        if len(self.prefixes) == 0:
            return True
        any_prefix_matched = any(
            (
                url.startswith(
                    '{base_url}{prefix}'.format(
                        base_url=self.base_url, prefix=prefix
                    )
                )
                for prefix in self.prefixes
            )
        )
        return self.prefix_predicate(any_prefix_matched)

    def url(self, name: str) -> str:
        url = super().url(name)
        return self.pre_sign_url(url, seconds=self.expires_seconds)

    def pre_sign_url(self, url: str, seconds: int) -> str:
        """Generates pre-signed url with md5 token"""
        # skip if it's not specified in `self.path_prefixes`
        if not self._is_secure_path(url):
            return url

        hashable_url = url.replace(self.not_hashable_prefix, '')

        current_time = datetime.datetime.now(tz=datetime.timezone.utc)
        timestamp = utils.gen_expires(current_time, seconds)
        token = utils.gen_hash(hashable_url, timestamp, self.nginx_secret_key)
        params = urllib.parse.urlencode(
            {
                self.token_field_name: token,
                self.expires_field_name: timestamp,
            }
        )
        return '{url}?{params}'.format(url=url, params=params)
