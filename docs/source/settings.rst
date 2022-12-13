Settings
========

This page describes all existing settings of th module which we can override
if it needs and make the project more customized.


- ``SECURE_LINK_SECRET_KEY``

Your specific secret string which Nginx is going to use in ``secure_link_md5`` directive.

- ``SECURE_LINK_TOKEN_FIELD`` (optional, default: ``token``)

Your custom name of the hash GET-parameter (?token=xyz)

- ``SECURE_LINK_EXPIRES_FIELD`` (optional, default: ``expires``)

Your custom name of expiration timestamp GET-parameter  (?expires=1599215210)

- ``SECURE_LINK_EXPIRATION_SECONDS`` (optional, default: ``86400``- 1 day)

Your custom value of expiration seconds. Any pre-signed link will be expired after ``SECURE_LINK_EXPIRATION_SECONDS``.

- ``SECURE_LINK_PRIVATE_PREFIXES`` (optional, default: ``[]``)

List of private paths without ``MEDIA_URL`` prefix. Just leave it empty for making all media urls private. Example:

.. code-block:: python

    MEDIA_URL = '/media/'
    SECURE_LINK_PRIVATE_PREFIXES = [
        'documents/',
        'reports/',
    ]

In such case all ``/media/documents/`` and ``/media/reports/`` urls will be private and pre-signed by using token and expiration time. If any of existing prefixes on the project are not listed in ``SECURE_LINK_PRIVATE_PREFIXES``, so the url will be public.

- ``SECURE_LINK_PUBLIC_PREFIXES`` (optional, default: ``[]``)

List of private paths without ``MEDIA_URL`` prefix. Example:

.. code-block:: python

    MEDIA_URL = '/media/'
    SECURE_LINK_PUBLIC_PREFIXES = [
        'avatars/',
        'shared/',
    ]

In such case only ``/media/avatars/`` and ``/media/shared/`` urls will be public and generated without pre-signed urls. All other urls, will be private and pre-signed by using token and expiration time.

**Important** If you want to keep all media files privately, ``SECURE_LINK_PRIVATE_PREFIXES`` and ``SECURE_LINK_PUBLIC_PREFIXES`` should be ``[]``.
