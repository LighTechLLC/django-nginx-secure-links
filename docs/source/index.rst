Welcome to django-nginx-secure-links documentation!
====================================================

django-nginx-secure-links module is a Django extension for using `ngx_http_secure_link_module <http://nginx.org/en/docs/http/ngx_http_secure_link_module.html>`_.
It provides private urls with expiration lifetime by implementing described logic of ngx_http_secure_link_module.
The major advantage of the extension is that Django delegates file serving on Nginx layer and does only pre-signed urls generation.


Check out the :doc:`quickstart` section for further information, including
how to :doc:`installation` the project.


Contents
--------

.. toctree::

   installation
   quickstart
   settings
   advanced