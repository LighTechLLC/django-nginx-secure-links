Installation
============

Installing from PyPI is as easy as doing:

.. code-block:: bash

    pip install django-nginx-secure-links

If you want to install it from source, grab the git repository from GitHub and run setup.py:

.. code-block:: bash

    git clone git://github.com/lighTechLLC/django-nginx-secure-links.git
    cd django-nginx-secure-links
    python setup.py install

Nginx module set up
===================

.. note::

    We need to follow this step only when Nginx is there, probably it will be
    when you work with real server. Since the project is under local development
    we do not need this instruction.

**Option 1**

Install using apt (Ubuntu example):

.. code-block:: bash

    sudo apt install nginx-extras

**Option 2**

Build from sources:

.. code-block:: bash

    ./configure .... --with-http_secure_link_module


