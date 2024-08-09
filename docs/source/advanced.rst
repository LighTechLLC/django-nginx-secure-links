Advanced Usage
==============

**Example 1:** We are going to use our own server directory and url prefix instead
of ``settings.MEDIA_ROOT`` / ``settings.MEDIA_URL``.
The example is going to use all default ``settings.SECURE_LINK_*``

.. code-block:: python

    from nginx_secure_links.storages import FileStorage

    storage = FileStorage(location='/var/www/personal_data/', base_url='/personal/')
    storage.url('profile.pdf')

**Example 2**: We are going to use custom storage with all overridden settings.

.. code-block:: python

  from nginx_secure_links.storages import FileStorage

  storage = FileStorage(
        location='/var/www/personal_data/',
        base_url='/personal/'
        nginx_secret_key='91rdywY7d4494X',
        expires_field_name='expires_timestamp',
        token_field_name='hash',
        private_prefixes=[],
        public_prefixes=[],
        expires_seconds=60 * 60,  # 60min
    ) # all private
    storage.url('profile.pdf')  # /personal/profile.pdf?hash=mlkiuhbhu83d&expires_timestamp=2147483647


**Example 3:** ``FileStorage`` supports to use custom lifetime for each specific file.
The example is going to use all default ``settings.SECURE_LINK_*``

.. code-block:: python

    from nginx_secure_links.storages import FileStorage

    storage = FileStorage(location='/var/www/personal_data/', base_url='/personal/')
    # link expires in 60 seconds
    url1 = storage.url('profile.pdf', lifetime=60)
    # link expires in 180 seconds
    url2 = storage.url('profile.pdf', lifetime=60 * 3)
    # link never expires
    url3 = storage.url('profile.pdf', lifetime=0)
