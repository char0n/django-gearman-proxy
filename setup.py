# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

import django_gearman_proxy


def read(fname):
    """Utility function to read the README file.

    Used for the long_description. It's nice, because now 1) we have a top level
    README file and 2) it's easier to type in the README file than to put a raw
    string in below ...

    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='django-gearman-proxy',
    version=django_gearman_proxy.VERSION,
    description='Proxy backends/workers for asynchronous email and sms sending using gearman as message queue.',
    long_description=read('README.rst'),
    author=u'Vladimír Gorej',
    author_email='gorej@codescale.net',
    url='http://www.codescale.net/en/community#django-gearman-proxy',
    download_url='http://github.com/codescaleinc/django-gearman-proxy/tarball/master',
    license='BSD',
    keywords = 'django gearman email sms asynchronous message queue',
    packages=find_packages('.'),
    install_requires=['django', 'django_gearman_commands', 'smssluzbacz-api', 'django-sendsms'],
    dependency_links = ['http://github.com/Yelp/python-gearman/tarball/master#egg=gearman-dev'],
    platforms='any',
    test_suite='django_gearman_proxy.tests',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
        'Topic :: Internet :: WWW/HTTP'
    ]
)