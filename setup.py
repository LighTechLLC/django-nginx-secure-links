# -*- coding: utf-8 -*-
import os

from setuptools import setup

version = __import__('nginx_secure_links').__version__

long_description = """django-nginx-secure-links extends django
 FileSystemStorage by implementing secure links based on temporal links and uses
 Nginx secure links module for that. See the project page for more information:
  http://github.com/lighTechLLC/django-nginx-secure-links"""

if os.path.isfile('README.rst'):
    with open('README.rst') as f:
        long_description = f.read()

setup(
    name='django-nginx-secure-links',
    version=version,
    description="Django storage based on Nginx secure links module",
    long_description_content_type='text/x-rst',
    long_description=long_description,
    author='Eugene Hatsko',
    author_email='',
    maintainer='Eugene Hatsko',
    maintainer_email='ehatsko@gmail.com',
    url='http://github.com/lighTechLLC/django-nginx-secure-links',
    license='MIT License',
    platforms=['any'],
    packages=[
        'nginx_secure_links',
        'nginx_secure_links.management',
    ],
    python_requires=">=3.6",
    install_requires=["Django>=3.2"],
    extras_require={},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ],
    project_urls={
    },
)
